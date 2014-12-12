#define DEBUG_TYPE "mallocs_nonnull"

#include <map>
#include <queue>
#include <set>

#include "llvm/ADT/Statistic.h"
#include "llvm/Analysis/Dominators.h"
#include "llvm/Analysis/PostDominators.h"
#include "llvm/Assembly/Writer.h"
#include "llvm/Constants.h"
#include "llvm/Function.h"
#include "llvm/Instructions.h"
#include "llvm/Module.h"
#include "llvm/Operator.h"
#include "llvm/Pass.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/InstIterator.h"
#include "llvm/Support/InstVisitor.h"
#include "llvm/Support/raw_ostream.h"

STATISTIC(NumReplaced, "Number of comparisons elided");

using namespace llvm;
using namespace std;

namespace {

    // TODO Copy-paste
    static bool isMallocCall(const CallInst *CI) {
        if (!CI)
            return false;

        Function *Callee = CI->getCalledFunction();
        if (Callee == 0 || !Callee->isDeclaration())
            return false;
        if (Callee->getName() != "malloc" &&
                Callee->getName() != "my_malloc" &&
                Callee->getName() != "_Znwj" && // operator new(unsigned int)
                Callee->getName() != "_Znwm" && // operator new(unsigned long)
                Callee->getName() != "_Znaj" && // operator new[](unsigned int)
                Callee->getName() != "_Znam")   // operator new[](unsigned long)
                return false;

        // Check malloc prototype.
        // FIXME: workaround for PR5130, this will be obsolete when a nobuiltin 
        // attribute will exist.
        FunctionType *FTy = Callee->getFunctionType();
        return FTy->getReturnType() == Type::getInt8PtrTy(FTy->getContext()) &&
            FTy->getNumParams() == 1 &&
            (FTy->getParamType(0)->isIntegerTy(32) ||
             FTy->getParamType(0)->isIntegerTy(64));
    }

    /// isFreeCall - Returns non-null if the value is a call to the builtin free()
    static const CallInst *isFreeCall(const Value *I) {
        const CallInst *CI = dyn_cast<CallInst>(I);
        if (!CI)
            return 0;
        Function *Callee = CI->getCalledFunction();
        if (Callee == 0 || !Callee->isDeclaration())
            return 0;

        if (Callee->getName() != "free" &&
                Callee->getName() != "my_free" &&
                Callee->getName() != "_ZdlPv" && // operator delete(void*)
                Callee->getName() != "_ZdaPv")   // operator delete[](void*)
                return 0;

        // Check free prototype.
        // FIXME: workaround for PR5130, this will be obsolete when a nobuiltin 
        // attribute will exist.
        FunctionType *FTy = Callee->getFunctionType();
        if (!FTy->getReturnType()->isVoidTy())
            return 0;
        if (FTy->getNumParams() != 1)
            return 0;
        if (FTy->getParamType(0) != Type::getInt8PtrTy(Callee->getContext()))
            return 0;

        return CI;
    }

    class ComparisonFinder : public InstVisitor<ComparisonFinder, bool> {
    private:
        int num_changed;
        deque<Instruction*> to_process;
        Instruction* processing;

    public:
        ComparisonFinder(CallInst* malloc) : num_changed(0) {
            to_process.push_back(malloc);
        }

        int elide_comparisons() {
            while (to_process.size()) {
                processing = to_process.front();
                to_process.pop_front();

                DEBUG(errs() << "processing: " << *processing << '\n');
                bool changed = false;
                do {
                    changed = false;
                    for (Value::use_iterator use_it = processing->use_begin(), use_end = processing->use_end(); use_it != use_end; ++use_it) {
                        DEBUG(errs() << "looking at: " << **use_it << '\n');
                        changed = visit(cast<Instruction>(*use_it));
                        if (changed)
                            break;
                    }
                } while (changed);
            }
            return num_changed;
        }

        bool visitBitCastInst(BitCastInst &inst) {
            to_process.push_back(&inst);
            return false;
        }

        bool visitICmpInst(ICmpInst &inst) {
            DEBUG(errs() << "got icmp instruction!  " << inst << '\n');

            bool changed = false;
            if (inst.getPredicate() == CmpInst::ICMP_EQ) {
                assert(inst.getNumOperands() == 2);

                if (inst.getOperand(1) == processing) {
                    inst.swapOperands();
                    changed = true;
                }
                assert(dyn_cast<Instruction>(inst.getOperand(0)) == processing);
                Value* other = inst.getOperand(1);
                if (isa<ConstantPointerNull>(other)) {
                    DEBUG(errs() << "doing replacement\n");

                    Value* new_value = ConstantInt::getFalse(other->getContext());
                    inst.replaceAllUsesWith(new_value);
                    inst.eraseFromParent();
                    changed = true;
                }
            }
            return changed;
        }

        bool visitInstruction(Instruction &inst) {
            DEBUG(errs() << "got misc instruction: " << inst << '\n');
            return false;
        }
    };

    class MallocsNonNullPass : public FunctionPass {
        public:
        static char ID;
        MallocsNonNullPass() : FunctionPass(ID) {}

        virtual void getAnalysisUsage(AnalysisUsage &info) const {
            info.setPreservesCFG();
        }

        virtual bool runOnFunction(Function &F) {
            int num_changed = 0;
            for (inst_iterator inst_it = inst_begin(F), _inst_end = inst_end(F); inst_it != _inst_end; ++inst_it) {
                if (!isMallocCall(dyn_cast<CallInst>(&*inst_it)))
                    continue;

                DEBUG(errs() << "\nFound malloc call:\n" << *inst_it << '\n');
                num_changed += ComparisonFinder(cast<CallInst>(&*inst_it)).elide_comparisons();
            }

            NumReplaced += num_changed;
            return num_changed > 0;
        }

    };
}

char MallocsNonNullPass::ID = 0;
static RegisterPass<MallocsNonNullPass> X("mallocs_nonnull", "Use the fact that malloc() doesnt return NULL", true, false);


