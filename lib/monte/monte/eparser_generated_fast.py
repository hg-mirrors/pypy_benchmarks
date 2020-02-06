from ometa.runtime import OMetaGrammarBase as GrammarBase
class BaseEParser(GrammarBase):
    def rule_updocLine(self):
        _locals = {'self': self}
        self.locals['updocLine'] = _locals
        def _G_consumedby_1():
            def _G_or_2():
                _G_exactly_3, lastError = self.exactly('?')
                return (_G_exactly_3, self.currentError)
            def _G_or_4():
                _G_exactly_5, lastError = self.exactly('#')
                return (_G_exactly_5, self.currentError)
            def _G_or_6():
                _G_exactly_7, lastError = self.exactly('>')
                return (_G_exactly_7, self.currentError)
            _G_or_8, lastError = self._or([_G_or_2, _G_or_4, _G_or_6])
            def _G_many_9():
                def _G_not_10():
                    def _G_or_11():
                        _G_exactly_12, lastError = self.exactly('\n')
                        return (_G_exactly_12, self.currentError)
                    def _G_or_13():
                        _G_exactly_14, lastError = self.exactly('\r')
                        return (_G_exactly_14, self.currentError)
                    _G_or_15, lastError = self._or([_G_or_11, _G_or_13])
                    return (_G_or_15, self.currentError)
                _G_not_16, lastError = self._not(_G_not_10)
                _G_apply_17, lastError = self._apply(self.rule_anything, "anything", [])
                return (_G_apply_17, self.currentError)
            _G_many_18, lastError = self.many(_G_many_9)
            return (_G_many_18, self.currentError)
        _G_consumedby_19, lastError = self.consumedby(_G_consumedby_1)
        _locals['txt'] = _G_consumedby_19
        _G_apply_20, lastError = self._apply(self.rule_eol, "eol", [])
        _G_python_21, lastError = eval('txt', self.globals, _locals), None
        return (_G_python_21, self.currentError)


    def rule_updoc(self):
        _locals = {'self': self}
        self.locals['updoc'] = _locals
        _G_exactly_22, lastError = self.exactly('?')
        def _G_many_23():
            def _G_not_24():
                def _G_or_25():
                    _G_exactly_26, lastError = self.exactly('\n')
                    return (_G_exactly_26, self.currentError)
                def _G_or_27():
                    _G_exactly_28, lastError = self.exactly('\r')
                    return (_G_exactly_28, self.currentError)
                _G_or_29, lastError = self._or([_G_or_25, _G_or_27])
                return (_G_or_29, self.currentError)
            _G_not_30, lastError = self._not(_G_not_24)
            _G_apply_31, lastError = self._apply(self.rule_anything, "anything", [])
            return (_G_apply_31, self.currentError)
        _G_many_32, lastError = self.many(_G_many_23)
        def _G_optional_33():
            _G_apply_34, lastError = self._apply(self.rule_eol, "eol", [])
            def _G_many_35():
                def _G_or_36():
                    _G_apply_37, lastError = self._apply(self.rule_eol, "eol", [])
                    return (_G_apply_37, self.currentError)
                def _G_or_38():
                    _G_apply_39, lastError = self._apply(self.rule_updocLine, "updocLine", [])
                    return (_G_apply_39, self.currentError)
                _G_or_40, lastError = self._or([_G_or_36, _G_or_38])
                return (_G_or_40, self.currentError)
            _G_many_41, lastError = self.many(_G_many_35)
            def _G_or_42():
                _G_apply_43, lastError = self._apply(self.rule_spaces, "spaces", [])
                return (_G_apply_43, self.currentError)
            def _G_or_44():
                _G_apply_45, lastError = self._apply(self.rule_updocLine, "updocLine", [])
                return (_G_apply_45, self.currentError)
            _G_or_46, lastError = self._or([_G_or_42, _G_or_44])
            return (_G_or_46, self.currentError)
        def _G_optional_47():
            return (None, self.input.nullError())
        _G_or_48, lastError = self._or([_G_optional_33, _G_optional_47])
        return (_G_or_48, self.currentError)


    def rule_eolplus(self):
        _locals = {'self': self}
        self.locals['eolplus'] = _locals
        _G_apply_49, lastError = self._apply(self.rule_eol, "eol", [])
        def _G_optional_50():
            _G_apply_51, lastError = self._apply(self.rule_updoc, "updoc", [])
            return (_G_apply_51, self.currentError)
        def _G_optional_52():
            return (None, self.input.nullError())
        _G_or_53, lastError = self._or([_G_optional_50, _G_optional_52])
        return (_G_or_53, self.currentError)


    def rule_linesep(self):
        _locals = {'self': self}
        self.locals['linesep'] = _locals
        def _G_many1_54():
            _G_apply_55, lastError = self._apply(self.rule_eolplus, "eolplus", [])
            return (_G_apply_55, self.currentError)
        _G_many1_56, lastError = self.many(_G_many1_54, _G_many1_54())
        return (_G_many1_56, self.currentError)


    def rule_br(self):
        _locals = {'self': self}
        self.locals['br'] = _locals
        def _G_many_57():
            def _G_or_58():
                _G_apply_59, lastError = self._apply(self.rule_spaces, "spaces", [])
                _G_apply_60, lastError = self._apply(self.rule_eolplus, "eolplus", [])
                return (_G_apply_60, self.currentError)
            def _G_or_61():
                _G_apply_62, lastError = self._apply(self.rule_eolplus, "eolplus", [])
                return (_G_apply_62, self.currentError)
            _G_or_63, lastError = self._or([_G_or_58, _G_or_61])
            return (_G_or_63, self.currentError)
        _G_many_64, lastError = self.many(_G_many_57)
        return (_G_many_64, self.currentError)


    def rule_literal(self):
        _locals = {'self': self}
        self.locals['literal'] = _locals
        def _G_or_65():
            _G_apply_66, lastError = self._apply(self.rule_string, "string", [])
            return (_G_apply_66, self.currentError)
        def _G_or_67():
            _G_apply_68, lastError = self._apply(self.rule_character, "character", [])
            return (_G_apply_68, self.currentError)
        def _G_or_69():
            _G_apply_70, lastError = self._apply(self.rule_number, "number", [])
            return (_G_apply_70, self.currentError)
        _G_or_71, lastError = self._or([_G_or_65, _G_or_67, _G_or_69])
        _locals['x'] = _G_or_71
        _G_python_72, lastError = eval('t.LiteralExpr(x)', self.globals, _locals), None
        return (_G_python_72, self.currentError)


    def rule_identifier(self):
        _locals = {'self': self}
        self.locals['identifier'] = _locals
        _G_apply_73, lastError = self._apply(self.rule_spaces, "spaces", [])
        def _G_consumedby_74():
            def _G_or_75():
                _G_apply_76, lastError = self._apply(self.rule_letter, "letter", [])
                return (_G_apply_76, self.currentError)
            def _G_or_77():
                _G_exactly_78, lastError = self.exactly('_')
                return (_G_exactly_78, self.currentError)
            _G_or_79, lastError = self._or([_G_or_75, _G_or_77])
            def _G_many_80():
                def _G_or_81():
                    _G_apply_82, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    return (_G_apply_82, self.currentError)
                def _G_or_83():
                    _G_exactly_84, lastError = self.exactly('_')
                    return (_G_exactly_84, self.currentError)
                _G_or_85, lastError = self._or([_G_or_81, _G_or_83])
                return (_G_or_85, self.currentError)
            _G_many_86, lastError = self.many(_G_many_80)
            return (_G_many_86, self.currentError)
        _G_consumedby_87, lastError = self.consumedby(_G_consumedby_74)
        return (_G_consumedby_87, self.currentError)


    def rule_uri(self):
        _locals = {'self': self}
        self.locals['uri'] = _locals
        _G_python_88, lastError = '<', None
        _G_apply_89, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_88])
        _G_apply_90, lastError = self._apply(self.rule_uriScheme, "uriScheme", [])
        _locals['s'] = _G_apply_90
        _G_exactly_91, lastError = self.exactly(':')
        _G_apply_92, lastError = self._apply(self.rule_uriBody, "uriBody", [])
        _locals['b'] = _G_apply_92
        _G_exactly_93, lastError = self.exactly('>')
        _G_python_94, lastError = eval('t.URIExpr(s, b)', self.globals, _locals), None
        return (_G_python_94, self.currentError)


    def rule_uriGetter(self):
        _locals = {'self': self}
        self.locals['uriGetter'] = _locals
        _G_python_95, lastError = '<', None
        _G_apply_96, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_95])
        _G_apply_97, lastError = self._apply(self.rule_uriScheme, "uriScheme", [])
        _locals['s'] = _G_apply_97
        _G_exactly_98, lastError = self.exactly('>')
        _G_python_99, lastError = eval('t.URIGetter(s)', self.globals, _locals), None
        return (_G_python_99, self.currentError)


    def rule_uriScheme(self):
        _locals = {'self': self}
        self.locals['uriScheme'] = _locals
        def _G_consumedby_100():
            _G_apply_101, lastError = self._apply(self.rule_letter, "letter", [])
            def _G_many_102():
                def _G_or_103():
                    _G_apply_104, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                    return (_G_apply_104, self.currentError)
                def _G_or_105():
                    _G_exactly_106, lastError = self.exactly('_')
                    return (_G_exactly_106, self.currentError)
                def _G_or_107():
                    _G_exactly_108, lastError = self.exactly('+')
                    return (_G_exactly_108, self.currentError)
                def _G_or_109():
                    _G_exactly_110, lastError = self.exactly('-')
                    return (_G_exactly_110, self.currentError)
                def _G_or_111():
                    _G_exactly_112, lastError = self.exactly('.')
                    return (_G_exactly_112, self.currentError)
                _G_or_113, lastError = self._or([_G_or_103, _G_or_105, _G_or_107, _G_or_109, _G_or_111])
                return (_G_or_113, self.currentError)
            _G_many_114, lastError = self.many(_G_many_102)
            return (_G_many_114, self.currentError)
        _G_consumedby_115, lastError = self.consumedby(_G_consumedby_100)
        return (_G_consumedby_115, self.currentError)


    def rule_noun(self):
        _locals = {'self': self}
        self.locals['noun'] = _locals
        def _G_or_116():
            _G_apply_117, lastError = self._apply(self.rule_sourceHole, "sourceHole", [])
            return (_G_apply_117, self.currentError)
        def _G_or_118():
            _G_apply_119, lastError = self._apply(self.rule_justNoun, "justNoun", [])
            return (_G_apply_119, self.currentError)
        _G_or_120, lastError = self._or([_G_or_116, _G_or_118])
        return (_G_or_120, self.currentError)


    def rule_justNoun(self):
        _locals = {'self': self}
        self.locals['justNoun'] = _locals
        def _G_or_121():
            def _G_or_122():
                _G_apply_123, lastError = self._apply(self.rule_identifier, "identifier", [])
                _locals['id'] = _G_apply_123
                _G_python_124, lastError = eval('self.keywordCheck(id)', self.globals, _locals), None
                return (_G_python_124, self.currentError)
            def _G_or_125():
                _G_python_126, lastError = '::', None
                _G_apply_127, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_126])
                def _G_or_128():
                    _G_apply_129, lastError = self._apply(self.rule_string, "string", [])
                    return (_G_apply_129, self.currentError)
                def _G_or_130():
                    _G_apply_131, lastError = self._apply(self.rule_identifier, "identifier", [])
                    return (_G_apply_131, self.currentError)
                _G_or_132, lastError = self._or([_G_or_128, _G_or_130])
                _locals['x'] = _G_or_132
                _G_python_133, lastError = eval('x', self.globals, _locals), None
                return (_G_python_133, self.currentError)
            _G_or_134, lastError = self._or([_G_or_122, _G_or_125])
            _locals['n'] = _G_or_134
            _G_python_135, lastError = eval('t.NounExpr(n)', self.globals, _locals), None
            return (_G_python_135, self.currentError)
        def _G_or_136():
            _G_apply_137, lastError = self._apply(self.rule_uriGetter, "uriGetter", [])
            return (_G_apply_137, self.currentError)
        _G_or_138, lastError = self._or([_G_or_121, _G_or_136])
        return (_G_or_138, self.currentError)


    def rule_sourceHole(self):
        _locals = {'self': self}
        self.locals['sourceHole'] = _locals
        def _G_or_139():
            _G_python_140, lastError = '$', None
            _G_apply_141, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_140])
            _G_python_142, lastError = eval('self.valueHole()', self.globals, _locals), None
            _locals['v'] = _G_python_142
            _G_exactly_143, lastError = self.exactly('{')
            def _G_many1_144():
                _G_apply_145, lastError = self._apply(self.rule_digit, "digit", [])
                return (_G_apply_145, self.currentError)
            _G_many1_146, lastError = self.many(_G_many1_144, _G_many1_144())
            _locals['ds'] = _G_many1_146
            _G_exactly_147, lastError = self.exactly('}')
            _G_python_148, lastError = eval('t.QuasiLiteralExpr(v)', self.globals, _locals), None
            return (_G_python_148, self.currentError)
        def _G_or_149():
            _G_python_150, lastError = '@', None
            _G_apply_151, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_150])
            _G_python_152, lastError = eval('self.patternHole()', self.globals, _locals), None
            _locals['v'] = _G_python_152
            _G_exactly_153, lastError = self.exactly('{')
            def _G_many1_154():
                _G_apply_155, lastError = self._apply(self.rule_digit, "digit", [])
                return (_G_apply_155, self.currentError)
            _G_many1_156, lastError = self.many(_G_many1_154, _G_many1_154())
            _locals['ds'] = _G_many1_156
            _G_exactly_157, lastError = self.exactly('}')
            _G_python_158, lastError = eval('t.QuasiPatternExpr(v)', self.globals, _locals), None
            return (_G_python_158, self.currentError)
        _G_or_159, lastError = self._or([_G_or_139, _G_or_149])
        return (_G_or_159, self.currentError)


    def rule_quasiString(self):
        _locals = {'self': self}
        self.locals['quasiString'] = _locals
        _G_python_160, lastError = '`', None
        _G_apply_161, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_160])
        def _G_many_162():
            def _G_or_163():
                _G_apply_164, lastError = self._apply(self.rule_exprHole, "exprHole", [])
                return (_G_apply_164, self.currentError)
            def _G_or_165():
                _G_apply_166, lastError = self._apply(self.rule_pattHole, "pattHole", [])
                return (_G_apply_166, self.currentError)
            def _G_or_167():
                _G_apply_168, lastError = self._apply(self.rule_quasiText, "quasiText", [])
                return (_G_apply_168, self.currentError)
            _G_or_169, lastError = self._or([_G_or_163, _G_or_165, _G_or_167])
            return (_G_or_169, self.currentError)
        _G_many_170, lastError = self.many(_G_many_162)
        _locals['qs'] = _G_many_170
        _G_exactly_171, lastError = self.exactly('`')
        _G_python_172, lastError = eval('qs', self.globals, _locals), None
        return (_G_python_172, self.currentError)


    def rule_quasiText(self):
        _locals = {'self': self}
        self.locals['quasiText'] = _locals
        def _G_consumedby_173():
            def _G_many1_174():
                def _G_or_175():
                    def _G_not_176():
                        def _G_or_177():
                            _G_exactly_178, lastError = self.exactly('`')
                            return (_G_exactly_178, self.currentError)
                        def _G_or_179():
                            _G_exactly_180, lastError = self.exactly('$')
                            return (_G_exactly_180, self.currentError)
                        def _G_or_181():
                            _G_exactly_182, lastError = self.exactly('@')
                            return (_G_exactly_182, self.currentError)
                        _G_or_183, lastError = self._or([_G_or_177, _G_or_179, _G_or_181])
                        return (_G_or_183, self.currentError)
                    _G_not_184, lastError = self._not(_G_not_176)
                    _G_apply_185, lastError = self._apply(self.rule_anything, "anything", [])
                    return (_G_apply_185, self.currentError)
                def _G_or_186():
                    _G_exactly_187, lastError = self.exactly('`')
                    _G_exactly_188, lastError = self.exactly('`')
                    return (_G_exactly_188, self.currentError)
                def _G_or_189():
                    _G_exactly_190, lastError = self.exactly('$')
                    _G_exactly_191, lastError = self.exactly('$')
                    return (_G_exactly_191, self.currentError)
                def _G_or_192():
                    def _G_or_193():
                        _G_exactly_194, lastError = self.exactly('$')
                        return (_G_exactly_194, self.currentError)
                    def _G_or_195():
                        _G_exactly_196, lastError = self.exactly('@')
                        return (_G_exactly_196, self.currentError)
                    _G_or_197, lastError = self._or([_G_or_193, _G_or_195])
                    _G_exactly_198, lastError = self.exactly('\\')
                    _G_apply_199, lastError = self._apply(self.rule_escapedChar, "escapedChar", [])
                    return (_G_apply_199, self.currentError)
                def _G_or_200():
                    _G_exactly_201, lastError = self.exactly('@')
                    _G_exactly_202, lastError = self.exactly('@')
                    return (_G_exactly_202, self.currentError)
                _G_or_203, lastError = self._or([_G_or_175, _G_or_186, _G_or_189, _G_or_192, _G_or_200])
                return (_G_or_203, self.currentError)
            _G_many1_204, lastError = self.many(_G_many1_174, _G_many1_174())
            return (_G_many1_204, self.currentError)
        _G_consumedby_205, lastError = self.consumedby(_G_consumedby_173)
        _locals['qs'] = _G_consumedby_205
        _G_python_206, lastError = eval('t.QuasiText(qs.replace("``", "`"))', self.globals, _locals), None
        return (_G_python_206, self.currentError)


    def rule_exprHole(self):
        _locals = {'self': self}
        self.locals['exprHole'] = _locals
        _G_exactly_207, lastError = self.exactly('$')
        def _G_or_208():
            _G_exactly_209, lastError = self.exactly('{')
            _G_apply_210, lastError = self._apply(self.rule_br, "br", [])
            _G_apply_211, lastError = self._apply(self.rule_seq, "seq", [])
            _locals['s'] = _G_apply_211
            _G_exactly_212, lastError = self.exactly('}')
            _G_python_213, lastError = eval('t.QuasiExprHole(s)', self.globals, _locals), None
            return (_G_python_213, self.currentError)
        def _G_or_214():
            _G_exactly_215, lastError = self.exactly('_')
            _G_python_216, lastError = eval('noIgnoreExpressionHole()', self.globals, _locals), None
            return (_G_python_216, self.currentError)
        def _G_or_217():
            _G_apply_218, lastError = self._apply(self.rule_identifier, "identifier", [])
            _locals['n'] = _G_apply_218
            _G_python_219, lastError = eval('exprHoleKeywordCheck(n)', self.globals, _locals), None
            _G_python_220, lastError = eval('t.QuasiExprHole(t.NounExpr(n))', self.globals, _locals), None
            return (_G_python_220, self.currentError)
        _G_or_221, lastError = self._or([_G_or_208, _G_or_214, _G_or_217])
        return (_G_or_221, self.currentError)


    def rule_pattHole(self):
        _locals = {'self': self}
        self.locals['pattHole'] = _locals
        _G_exactly_222, lastError = self.exactly('@')
        def _G_or_223():
            _G_exactly_224, lastError = self.exactly('{')
            _G_apply_225, lastError = self._apply(self.rule_br, "br", [])
            _G_apply_226, lastError = self._apply(self.rule_pattern, "pattern", [])
            _locals['s'] = _G_apply_226
            _G_exactly_227, lastError = self.exactly('}')
            _G_python_228, lastError = eval('t.QuasiPatternHole(s)', self.globals, _locals), None
            return (_G_python_228, self.currentError)
        def _G_or_229():
            _G_exactly_230, lastError = self.exactly('_')
            _G_python_231, lastError = eval('noIgnorePatternHole()', self.globals, _locals), None
            return (_G_python_231, self.currentError)
        def _G_or_232():
            _G_apply_233, lastError = self._apply(self.rule_identifier, "identifier", [])
            _locals['n'] = _G_apply_233
            _G_python_234, lastError = eval('quasiHoleKeywordCheck(n)', self.globals, _locals), None
            _G_python_235, lastError = eval('t.QuasiPatternHole(t.FinalPattern(t.NounExpr(n), None))', self.globals, _locals), None
            return (_G_python_235, self.currentError)
        _G_or_236, lastError = self._or([_G_or_223, _G_or_229, _G_or_232])
        return (_G_or_236, self.currentError)


    def rule_reifyExpr(self):
        _locals = {'self': self}
        self.locals['reifyExpr'] = _locals
        def _G_or_237():
            _G_python_238, lastError = '&&', None
            _G_apply_239, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_238])
            _G_apply_240, lastError = self._apply(self.rule_verb, "verb", [])
            _locals['v'] = _G_apply_240
            _G_python_241, lastError = eval('t.BindingExpr(v)', self.globals, _locals), None
            return (_G_python_241, self.currentError)
        def _G_or_242():
            _G_python_243, lastError = '&', None
            _G_apply_244, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_243])
            _G_apply_245, lastError = self._apply(self.rule_verb, "verb", [])
            _locals['v'] = _G_apply_245
            _G_python_246, lastError = eval('t.SlotExpr(v)', self.globals, _locals), None
            return (_G_python_246, self.currentError)
        _G_or_247, lastError = self._or([_G_or_237, _G_or_242])
        return (_G_or_247, self.currentError)


    def rule_verb(self):
        _locals = {'self': self}
        self.locals['verb'] = _locals
        def _G_or_248():
            _G_apply_249, lastError = self._apply(self.rule_identifier, "identifier", [])
            return (_G_apply_249, self.currentError)
        def _G_or_250():
            _G_apply_251, lastError = self._apply(self.rule_string, "string", [])
            return (_G_apply_251, self.currentError)
        _G_or_252, lastError = self._or([_G_or_248, _G_or_250])
        return (_G_or_252, self.currentError)


    def rule_listAndMap(self):
        _locals = {'self': self}
        self.locals['listAndMap'] = _locals
        _G_python_253, lastError = '[', None
        _G_apply_254, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_253])
        def _G_or_255():
            _G_apply_256, lastError = self._apply(self.rule_assoc, "assoc", [])
            _locals['x'] = _G_apply_256
            def _G_many_257():
                _G_python_258, lastError = ',', None
                _G_apply_259, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_258])
                _G_apply_260, lastError = self._apply(self.rule_assoc, "assoc", [])
                return (_G_apply_260, self.currentError)
            _G_many_261, lastError = self.many(_G_many_257)
            _locals['xs'] = _G_many_261
            def _G_optional_262():
                _G_python_263, lastError = ',', None
                _G_apply_264, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_263])
                return (_G_apply_264, self.currentError)
            def _G_optional_265():
                return (None, self.input.nullError())
            _G_or_266, lastError = self._or([_G_optional_262, _G_optional_265])
            _G_exactly_267, lastError = self.exactly(']')
            _G_python_268, lastError = eval('t.MapExpr([x] + xs)', self.globals, _locals), None
            return (_G_python_268, self.currentError)
        def _G_or_269():
            _G_apply_270, lastError = self._apply(self.rule_seq, "seq", [])
            _locals['s'] = _G_apply_270
            def _G_many_271():
                _G_python_272, lastError = ',', None
                _G_apply_273, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_272])
                _G_apply_274, lastError = self._apply(self.rule_seq, "seq", [])
                return (_G_apply_274, self.currentError)
            _G_many_275, lastError = self.many(_G_many_271)
            _locals['ss'] = _G_many_275
            def _G_optional_276():
                _G_python_277, lastError = ',', None
                _G_apply_278, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_277])
                return (_G_apply_278, self.currentError)
            def _G_optional_279():
                return (None, self.input.nullError())
            _G_or_280, lastError = self._or([_G_optional_276, _G_optional_279])
            _G_exactly_281, lastError = self.exactly(']')
            _G_python_282, lastError = eval('t.ListExpr([s] + ss)', self.globals, _locals), None
            return (_G_python_282, self.currentError)
        def _G_or_283():
            _G_exactly_284, lastError = self.exactly(']')
            _G_python_285, lastError = eval('t.ListExpr([])', self.globals, _locals), None
            return (_G_python_285, self.currentError)
        _G_or_286, lastError = self._or([_G_or_255, _G_or_269, _G_or_283])
        return (_G_or_286, self.currentError)


    def rule_assoc(self):
        _locals = {'self': self}
        self.locals['assoc'] = _locals
        def _G_or_287():
            _G_apply_288, lastError = self._apply(self.rule_seq, "seq", [])
            _locals['k'] = _G_apply_288
            _G_python_289, lastError = '=>', None
            _G_apply_290, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_289])
            _G_apply_291, lastError = self._apply(self.rule_seq, "seq", [])
            _locals['v'] = _G_apply_291
            _G_python_292, lastError = eval('t.MapExprAssoc(k, v)', self.globals, _locals), None
            return (_G_python_292, self.currentError)
        def _G_or_293():
            _G_python_294, lastError = '=>', None
            _G_apply_295, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_294])
            def _G_or_296():
                _G_apply_297, lastError = self._apply(self.rule_noun, "noun", [])
                return (_G_apply_297, self.currentError)
            def _G_or_298():
                _G_apply_299, lastError = self._apply(self.rule_reifyExpr, "reifyExpr", [])
                return (_G_apply_299, self.currentError)
            _G_or_300, lastError = self._or([_G_or_296, _G_or_298])
            _locals['n'] = _G_or_300
            _G_python_301, lastError = eval('t.MapExprExport(n)', self.globals, _locals), None
            return (_G_python_301, self.currentError)
        def _G_or_302():
            _G_python_303, lastError = 'def', None
            _G_apply_304, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_303])
            _G_apply_305, lastError = self._apply(self.rule_noun, "noun", [])
            _locals['n'] = _G_apply_305
            def _G_not_306():
                _G_python_307, lastError = ':=', None
                _G_apply_308, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_307])
                return (_G_apply_308, self.currentError)
            _G_not_309, lastError = self._not(_G_not_306)
            _G_python_310, lastError = eval('throwSemanticHere("Reserved syntax: forward export")', self.globals, _locals), None
            return (_G_python_310, self.currentError)
        _G_or_311, lastError = self._or([_G_or_287, _G_or_293, _G_or_302])
        return (_G_or_311, self.currentError)


    def rule_prim(self):
        _locals = {'self': self}
        self.locals['prim'] = _locals
        def _G_or_312():
            _G_apply_313, lastError = self._apply(self.rule_literal, "literal", [])
            return (_G_apply_313, self.currentError)
        def _G_or_314():
            _G_apply_315, lastError = self._apply(self.rule_basic, "basic", [])
            return (_G_apply_315, self.currentError)
        def _G_or_316():
            def _G_optional_317():
                _G_apply_318, lastError = self._apply(self.rule_identifier, "identifier", [])
                return (_G_apply_318, self.currentError)
            def _G_optional_319():
                return (None, self.input.nullError())
            _G_or_320, lastError = self._or([_G_optional_317, _G_optional_319])
            _locals['n'] = _G_or_320
            _G_apply_321, lastError = self._apply(self.rule_quasiString, "quasiString", [])
            _locals['qs'] = _G_apply_321
            _G_python_322, lastError = eval('t.QuasiExpr(n, qs)', self.globals, _locals), None
            return (_G_python_322, self.currentError)
        def _G_or_323():
            _G_apply_324, lastError = self._apply(self.rule_noun, "noun", [])
            return (_G_apply_324, self.currentError)
        def _G_or_325():
            _G_apply_326, lastError = self._apply(self.rule_uri, "uri", [])
            return (_G_apply_326, self.currentError)
        def _G_or_327():
            _G_apply_328, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
            _locals['p'] = _G_apply_328
            def _G_or_329():
                _G_apply_330, lastError = self._apply(self.rule_quasiString, "quasiString", [])
                _locals['qs'] = _G_apply_330
                _G_python_331, lastError = eval('t.QuasiExpr(p, qs)', self.globals, _locals), None
                return (_G_python_331, self.currentError)
            def _G_or_332():
                _G_python_333, lastError = eval('p', self.globals, _locals), None
                return (_G_python_333, self.currentError)
            _G_or_334, lastError = self._or([_G_or_329, _G_or_332])
            return (_G_or_334, self.currentError)
        def _G_or_335():
            _G_apply_336, lastError = self._apply(self.rule_block, "block", [])
            _locals['b'] = _G_apply_336
            _G_python_337, lastError = eval('t.HideExpr(b)', self.globals, _locals), None
            return (_G_python_337, self.currentError)
        def _G_or_338():
            _G_apply_339, lastError = self._apply(self.rule_listAndMap, "listAndMap", [])
            return (_G_apply_339, self.currentError)
        _G_or_340, lastError = self._or([_G_or_312, _G_or_314, _G_or_316, _G_or_323, _G_or_325, _G_or_327, _G_or_335, _G_or_338])
        return (_G_or_340, self.currentError)


    def rule_parenExpr(self):
        _locals = {'self': self}
        self.locals['parenExpr'] = _locals
        _G_python_341, lastError = '(', None
        _G_apply_342, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_341])
        _G_apply_343, lastError = self._apply(self.rule_seq, "seq", [])
        _locals['s'] = _G_apply_343
        _G_python_344, lastError = ')', None
        _G_apply_345, lastError = self._apply(self.rule_token, "token", [_G_python_344])
        _G_python_346, lastError = eval('s', self.globals, _locals), None
        return (_G_python_346, self.currentError)


    def rule_block(self):
        _locals = {'self': self}
        self.locals['block'] = _locals
        _G_python_347, lastError = '{', None
        _G_apply_348, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_347])
        def _G_or_349():
            _G_apply_350, lastError = self._apply(self.rule_seq, "seq", [])
            return (_G_apply_350, self.currentError)
        def _G_or_351():
            _G_python_352, lastError = eval('t.SeqExpr([])', self.globals, _locals), None
            return (_G_python_352, self.currentError)
        _G_or_353, lastError = self._or([_G_or_349, _G_or_351])
        _locals['s'] = _G_or_353
        _G_python_354, lastError = '}', None
        _G_apply_355, lastError = self._apply(self.rule_token, "token", [_G_python_354])
        _G_python_356, lastError = eval('s', self.globals, _locals), None
        return (_G_python_356, self.currentError)


    def rule_seqSep(self):
        _locals = {'self': self}
        self.locals['seqSep'] = _locals
        def _G_many1_357():
            def _G_or_358():
                _G_python_359, lastError = ';', None
                _G_apply_360, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_359])
                return (_G_apply_360, self.currentError)
            def _G_or_361():
                _G_apply_362, lastError = self._apply(self.rule_linesep, "linesep", [])
                return (_G_apply_362, self.currentError)
            _G_or_363, lastError = self._or([_G_or_358, _G_or_361])
            return (_G_or_363, self.currentError)
        _G_many1_364, lastError = self.many(_G_many1_357, _G_many1_357())
        return (_G_many1_364, self.currentError)


    def rule_seq(self):
        _locals = {'self': self}
        self.locals['seq'] = _locals
        _G_apply_365, lastError = self._apply(self.rule_expr, "expr", [])
        _locals['e'] = _G_apply_365
        def _G_or_366():
            def _G_many1_367():
                _G_apply_368, lastError = self._apply(self.rule_seqSep, "seqSep", [])
                _G_apply_369, lastError = self._apply(self.rule_expr, "expr", [])
                return (_G_apply_369, self.currentError)
            _G_many1_370, lastError = self.many(_G_many1_367, _G_many1_367())
            _locals['es'] = _G_many1_370
            def _G_optional_371():
                _G_apply_372, lastError = self._apply(self.rule_seqSep, "seqSep", [])
                return (_G_apply_372, self.currentError)
            def _G_optional_373():
                return (None, self.input.nullError())
            _G_or_374, lastError = self._or([_G_optional_371, _G_optional_373])
            _G_python_375, lastError = eval('t.SeqExpr(list(filter(None, [e] + es)))', self.globals, _locals), None
            return (_G_python_375, self.currentError)
        def _G_or_376():
            def _G_optional_377():
                _G_apply_378, lastError = self._apply(self.rule_seqSep, "seqSep", [])
                return (_G_apply_378, self.currentError)
            def _G_optional_379():
                return (None, self.input.nullError())
            _G_or_380, lastError = self._or([_G_optional_377, _G_optional_379])
            _G_python_381, lastError = eval('e', self.globals, _locals), None
            return (_G_python_381, self.currentError)
        _G_or_382, lastError = self._or([_G_or_366, _G_or_376])
        return (_G_or_382, self.currentError)


    def rule_parenArgs(self):
        _locals = {'self': self}
        self.locals['parenArgs'] = _locals
        _G_python_383, lastError = '(', None
        _G_apply_384, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_383])
        _G_apply_385, lastError = self._apply(self.rule_args, "args", [])
        _locals['a'] = _G_apply_385
        _G_python_386, lastError = ')', None
        _G_apply_387, lastError = self._apply(self.rule_token, "token", [_G_python_386])
        _G_python_388, lastError = eval('a', self.globals, _locals), None
        return (_G_python_388, self.currentError)


    def rule_args(self):
        _locals = {'self': self}
        self.locals['args'] = _locals
        def _G_or_389():
            _G_apply_390, lastError = self._apply(self.rule_seq, "seq", [])
            _locals['s'] = _G_apply_390
            def _G_many_391():
                _G_python_392, lastError = ',', None
                _G_apply_393, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_392])
                _G_apply_394, lastError = self._apply(self.rule_seq, "seq", [])
                return (_G_apply_394, self.currentError)
            _G_many_395, lastError = self.many(_G_many_391)
            _locals['ss'] = _G_many_395
            _G_python_396, lastError = eval('[s] + ss', self.globals, _locals), None
            return (_G_python_396, self.currentError)
        def _G_or_397():
            _G_python_398, lastError = [], None
            return (_G_python_398, self.currentError)
        _G_or_399, lastError = self._or([_G_or_389, _G_or_397])
        return (_G_or_399, self.currentError)


    def rule_call(self):
        _locals = {'self': self}
        self.locals['call'] = _locals
        def _G_or_400():
            _G_apply_401, lastError = self._apply(self.rule_call, "call", [])
            _locals['c'] = _G_apply_401
            def _G_or_402():
                _G_python_403, lastError = '.', None
                _G_apply_404, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_403])
                _G_apply_405, lastError = self._apply(self.rule_verb, "verb", [])
                _locals['v'] = _G_apply_405
                def _G_or_406():
                    _G_apply_407, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
                    _locals['x'] = _G_apply_407
                    _G_python_408, lastError = eval('t.MethodCallExpr(c, v, x)', self.globals, _locals), None
                    return (_G_python_408, self.currentError)
                def _G_or_409():
                    _G_python_410, lastError = eval('t.VerbCurryExpr(c, v)', self.globals, _locals), None
                    return (_G_python_410, self.currentError)
                _G_or_411, lastError = self._or([_G_or_406, _G_or_409])
                return (_G_or_411, self.currentError)
            def _G_or_412():
                _G_python_413, lastError = '[', None
                _G_apply_414, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_413])
                _G_apply_415, lastError = self._apply(self.rule_args, "args", [])
                _locals['a'] = _G_apply_415
                _G_python_416, lastError = ']', None
                _G_apply_417, lastError = self._apply(self.rule_token, "token", [_G_python_416])
                _G_python_418, lastError = eval('t.GetExpr(c, a)', self.globals, _locals), None
                return (_G_python_418, self.currentError)
            def _G_or_419():
                _G_apply_420, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
                _locals['x'] = _G_apply_420
                _G_python_421, lastError = eval('t.FunctionCallExpr(c, x)', self.globals, _locals), None
                return (_G_python_421, self.currentError)
            def _G_or_422():
                _G_python_423, lastError = '<-', None
                _G_apply_424, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_423])
                def _G_or_425():
                    _G_apply_426, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
                    _locals['x'] = _G_apply_426
                    _G_python_427, lastError = eval('t.FunctionSendExpr(c, x)', self.globals, _locals), None
                    return (_G_python_427, self.currentError)
                def _G_or_428():
                    _G_apply_429, lastError = self._apply(self.rule_verb, "verb", [])
                    _locals['v'] = _G_apply_429
                    def _G_or_430():
                        _G_apply_431, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
                        _locals['x'] = _G_apply_431
                        _G_python_432, lastError = eval('t.MethodSendExpr(c, v, x)', self.globals, _locals), None
                        return (_G_python_432, self.currentError)
                    def _G_or_433():
                        _G_python_434, lastError = eval('t.SendCurryExpr(c, v)', self.globals, _locals), None
                        return (_G_python_434, self.currentError)
                    _G_or_435, lastError = self._or([_G_or_430, _G_or_433])
                    return (_G_or_435, self.currentError)
                _G_or_436, lastError = self._or([_G_or_425, _G_or_428])
                return (_G_or_436, self.currentError)
            _G_or_437, lastError = self._or([_G_or_402, _G_or_412, _G_or_419, _G_or_422])
            return (_G_or_437, self.currentError)
        def _G_or_438():
            _G_apply_439, lastError = self._apply(self.rule_prim, "prim", [])
            return (_G_apply_439, self.currentError)
        _G_or_440, lastError = self._or([_G_or_400, _G_or_438])
        return (_G_or_440, self.currentError)


    def rule_prefix(self):
        _locals = {'self': self}
        self.locals['prefix'] = _locals
        def _G_or_441():
            _G_apply_442, lastError = self._apply(self.rule_call, "call", [])
            return (_G_apply_442, self.currentError)
        def _G_or_443():
            _G_python_444, lastError = '-', None
            _G_apply_445, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_444])
            _G_apply_446, lastError = self._apply(self.rule_call, "call", [])
            _locals['c'] = _G_apply_446
            _G_python_447, lastError = eval('t.Minus(c)', self.globals, _locals), None
            return (_G_python_447, self.currentError)
        def _G_or_448():
            _G_python_449, lastError = '!', None
            _G_apply_450, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_449])
            _G_apply_451, lastError = self._apply(self.rule_call, "call", [])
            _locals['c'] = _G_apply_451
            _G_python_452, lastError = eval('t.LogicalNot(c)', self.globals, _locals), None
            return (_G_python_452, self.currentError)
        def _G_or_453():
            _G_python_454, lastError = '~', None
            _G_apply_455, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_454])
            _G_apply_456, lastError = self._apply(self.rule_call, "call", [])
            _locals['c'] = _G_apply_456
            _G_python_457, lastError = eval('t.BinaryNot(c)', self.globals, _locals), None
            return (_G_python_457, self.currentError)
        def _G_or_458():
            _G_apply_459, lastError = self._apply(self.rule_reifyExpr, "reifyExpr", [])
            return (_G_apply_459, self.currentError)
        def _G_or_460():
            _G_python_461, lastError = '&', None
            _G_apply_462, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_461])
            _G_apply_463, lastError = self._apply(self.rule_call, "call", [])
            _G_python_464, lastError = eval('throwSemanticHere("reserved: unary prefix \'&\' applied to non-noun lValue")', self.globals, _locals), None
            return (_G_python_464, self.currentError)
        _G_or_465, lastError = self._or([_G_or_441, _G_or_443, _G_or_448, _G_or_453, _G_or_458, _G_or_460])
        return (_G_or_465, self.currentError)


    def rule_pow(self):
        _locals = {'self': self}
        self.locals['pow'] = _locals
        _G_apply_466, lastError = self._apply(self.rule_prefix, "prefix", [])
        _locals['x'] = _G_apply_466
        def _G_or_467():
            _G_python_468, lastError = '**', None
            _G_apply_469, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_468])
            _G_apply_470, lastError = self._apply(self.rule_prefix, "prefix", [])
            _locals['y'] = _G_apply_470
            _G_python_471, lastError = eval('t.Pow(x, y)', self.globals, _locals), None
            return (_G_python_471, self.currentError)
        def _G_or_472():
            _G_python_473, lastError = eval('x', self.globals, _locals), None
            return (_G_python_473, self.currentError)
        _G_or_474, lastError = self._or([_G_or_467, _G_or_472])
        return (_G_or_474, self.currentError)


    def rule_mult(self):
        _locals = {'self': self}
        self.locals['mult'] = _locals
        def _G_or_475():
            _G_apply_476, lastError = self._apply(self.rule_mult, "mult", [])
            _locals['x'] = _G_apply_476
            def _G_or_477():
                _G_python_478, lastError = '*', None
                _G_apply_479, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_478])
                _G_apply_480, lastError = self._apply(self.rule_pow, "pow", [])
                _locals['y'] = _G_apply_480
                _G_python_481, lastError = eval('t.Multiply(x, y)', self.globals, _locals), None
                return (_G_python_481, self.currentError)
            def _G_or_482():
                _G_python_483, lastError = '/', None
                _G_apply_484, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_483])
                _G_apply_485, lastError = self._apply(self.rule_pow, "pow", [])
                _locals['y'] = _G_apply_485
                _G_python_486, lastError = eval('t.Divide(x, y)', self.globals, _locals), None
                return (_G_python_486, self.currentError)
            def _G_or_487():
                _G_python_488, lastError = '//', None
                _G_apply_489, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_488])
                _G_apply_490, lastError = self._apply(self.rule_pow, "pow", [])
                _locals['y'] = _G_apply_490
                _G_python_491, lastError = eval('t.FloorDivide(x, y)', self.globals, _locals), None
                return (_G_python_491, self.currentError)
            def _G_or_492():
                _G_python_493, lastError = '%', None
                _G_apply_494, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_493])
                _G_apply_495, lastError = self._apply(self.rule_pow, "pow", [])
                _locals['y'] = _G_apply_495
                _G_python_496, lastError = eval('t.Remainder(x, y)', self.globals, _locals), None
                return (_G_python_496, self.currentError)
            def _G_or_497():
                _G_python_498, lastError = '%%', None
                _G_apply_499, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_498])
                _G_apply_500, lastError = self._apply(self.rule_pow, "pow", [])
                _locals['y'] = _G_apply_500
                _G_python_501, lastError = eval('t.Mod(x, y)', self.globals, _locals), None
                return (_G_python_501, self.currentError)
            _G_or_502, lastError = self._or([_G_or_477, _G_or_482, _G_or_487, _G_or_492, _G_or_497])
            return (_G_or_502, self.currentError)
        def _G_or_503():
            _G_apply_504, lastError = self._apply(self.rule_pow, "pow", [])
            return (_G_apply_504, self.currentError)
        _G_or_505, lastError = self._or([_G_or_475, _G_or_503])
        return (_G_or_505, self.currentError)


    def rule_add(self):
        _locals = {'self': self}
        self.locals['add'] = _locals
        def _G_or_506():
            _G_apply_507, lastError = self._apply(self.rule_add, "add", [])
            _locals['x'] = _G_apply_507
            def _G_or_508():
                _G_python_509, lastError = '+', None
                _G_apply_510, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_509])
                _G_apply_511, lastError = self._apply(self.rule_mult, "mult", [])
                _locals['y'] = _G_apply_511
                _G_python_512, lastError = eval('t.Add(x, y)', self.globals, _locals), None
                return (_G_python_512, self.currentError)
            def _G_or_513():
                _G_python_514, lastError = '-', None
                _G_apply_515, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_514])
                _G_apply_516, lastError = self._apply(self.rule_mult, "mult", [])
                _locals['y'] = _G_apply_516
                _G_python_517, lastError = eval('t.Subtract(x, y)', self.globals, _locals), None
                return (_G_python_517, self.currentError)
            _G_or_518, lastError = self._or([_G_or_508, _G_or_513])
            return (_G_or_518, self.currentError)
        def _G_or_519():
            _G_apply_520, lastError = self._apply(self.rule_mult, "mult", [])
            return (_G_apply_520, self.currentError)
        _G_or_521, lastError = self._or([_G_or_506, _G_or_519])
        return (_G_or_521, self.currentError)


    def rule_shift(self):
        _locals = {'self': self}
        self.locals['shift'] = _locals
        def _G_or_522():
            _G_apply_523, lastError = self._apply(self.rule_shift, "shift", [])
            _locals['x'] = _G_apply_523
            def _G_or_524():
                _G_python_525, lastError = '<<', None
                _G_apply_526, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_525])
                _G_apply_527, lastError = self._apply(self.rule_add, "add", [])
                _locals['y'] = _G_apply_527
                _G_python_528, lastError = eval('t.ShiftLeft(x, y)', self.globals, _locals), None
                return (_G_python_528, self.currentError)
            def _G_or_529():
                _G_python_530, lastError = '>>', None
                _G_apply_531, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_530])
                _G_apply_532, lastError = self._apply(self.rule_add, "add", [])
                _locals['y'] = _G_apply_532
                _G_python_533, lastError = eval('t.ShiftRight(x, y)', self.globals, _locals), None
                return (_G_python_533, self.currentError)
            _G_or_534, lastError = self._or([_G_or_524, _G_or_529])
            return (_G_or_534, self.currentError)
        def _G_or_535():
            _G_apply_536, lastError = self._apply(self.rule_add, "add", [])
            return (_G_apply_536, self.currentError)
        _G_or_537, lastError = self._or([_G_or_522, _G_or_535])
        return (_G_or_537, self.currentError)


    def rule_interval(self):
        _locals = {'self': self}
        self.locals['interval'] = _locals
        _G_apply_538, lastError = self._apply(self.rule_shift, "shift", [])
        _locals['x'] = _G_apply_538
        def _G_or_539():
            _G_python_540, lastError = '..!', None
            _G_apply_541, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_540])
            _G_apply_542, lastError = self._apply(self.rule_shift, "shift", [])
            _locals['y'] = _G_apply_542
            _G_python_543, lastError = eval('t.Till(x, y)', self.globals, _locals), None
            return (_G_python_543, self.currentError)
        def _G_or_544():
            _G_python_545, lastError = '..', None
            _G_apply_546, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_545])
            _G_apply_547, lastError = self._apply(self.rule_shift, "shift", [])
            _locals['y'] = _G_apply_547
            _G_python_548, lastError = eval('t.Thru(x, y)', self.globals, _locals), None
            return (_G_python_548, self.currentError)
        def _G_or_549():
            _G_python_550, lastError = eval('x', self.globals, _locals), None
            return (_G_python_550, self.currentError)
        _G_or_551, lastError = self._or([_G_or_539, _G_or_544, _G_or_549])
        return (_G_or_551, self.currentError)


    def rule_order(self):
        _locals = {'self': self}
        self.locals['order'] = _locals
        _G_apply_552, lastError = self._apply(self.rule_interval, "interval", [])
        _locals['x'] = _G_apply_552
        def _G_or_553():
            _G_python_554, lastError = '>', None
            _G_apply_555, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_554])
            _G_apply_556, lastError = self._apply(self.rule_interval, "interval", [])
            _locals['y'] = _G_apply_556
            _G_python_557, lastError = eval('t.GreaterThan(x, y)', self.globals, _locals), None
            return (_G_python_557, self.currentError)
        def _G_or_558():
            _G_python_559, lastError = '>=', None
            _G_apply_560, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_559])
            _G_apply_561, lastError = self._apply(self.rule_interval, "interval", [])
            _locals['y'] = _G_apply_561
            _G_python_562, lastError = eval('t.GreaterThanEqual(x, y)', self.globals, _locals), None
            return (_G_python_562, self.currentError)
        def _G_or_563():
            _G_python_564, lastError = '<=>', None
            _G_apply_565, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_564])
            _G_apply_566, lastError = self._apply(self.rule_interval, "interval", [])
            _locals['y'] = _G_apply_566
            _G_python_567, lastError = eval('t.AsBigAs(x, y)', self.globals, _locals), None
            return (_G_python_567, self.currentError)
        def _G_or_568():
            _G_python_569, lastError = '<=', None
            _G_apply_570, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_569])
            _G_apply_571, lastError = self._apply(self.rule_interval, "interval", [])
            _locals['y'] = _G_apply_571
            _G_python_572, lastError = eval('t.LessThanEqual(x, y)', self.globals, _locals), None
            return (_G_python_572, self.currentError)
        def _G_or_573():
            _G_python_574, lastError = '<', None
            _G_apply_575, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_574])
            _G_apply_576, lastError = self._apply(self.rule_interval, "interval", [])
            _locals['y'] = _G_apply_576
            _G_python_577, lastError = eval('t.LessThan(x, y)', self.globals, _locals), None
            return (_G_python_577, self.currentError)
        def _G_or_578():
            _G_python_579, lastError = ':', None
            _G_apply_580, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_579])
            _G_apply_581, lastError = self._apply(self.rule_guard, "guard", [])
            _locals['g'] = _G_apply_581
            _G_python_582, lastError = eval('t.Coerce(x, g)', self.globals, _locals), None
            return (_G_python_582, self.currentError)
        def _G_or_583():
            _G_python_584, lastError = eval('x', self.globals, _locals), None
            return (_G_python_584, self.currentError)
        _G_or_585, lastError = self._or([_G_or_553, _G_or_558, _G_or_563, _G_or_568, _G_or_573, _G_or_578, _G_or_583])
        return (_G_or_585, self.currentError)


    def rule_logical(self):
        _locals = {'self': self}
        self.locals['logical'] = _locals
        def _G_or_586():
            _G_apply_587, lastError = self._apply(self.rule_band, "band", [])
            return (_G_apply_587, self.currentError)
        def _G_or_588():
            _G_apply_589, lastError = self._apply(self.rule_bor, "bor", [])
            return (_G_apply_589, self.currentError)
        def _G_or_590():
            _G_apply_591, lastError = self._apply(self.rule_order, "order", [])
            _locals['x'] = _G_apply_591
            def _G_or_592():
                _G_python_593, lastError = '=~', None
                _G_apply_594, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_593])
                _G_apply_595, lastError = self._apply(self.rule_pattern, "pattern", [])
                _locals['p'] = _G_apply_595
                _G_python_596, lastError = eval('t.MatchBind(x, p)', self.globals, _locals), None
                return (_G_python_596, self.currentError)
            def _G_or_597():
                _G_python_598, lastError = '!~', None
                _G_apply_599, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_598])
                _G_apply_600, lastError = self._apply(self.rule_pattern, "pattern", [])
                _locals['p'] = _G_apply_600
                _G_python_601, lastError = eval('t.Mismatch(x, p)', self.globals, _locals), None
                return (_G_python_601, self.currentError)
            def _G_or_602():
                _G_python_603, lastError = '==', None
                _G_apply_604, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_603])
                _G_apply_605, lastError = self._apply(self.rule_order, "order", [])
                _locals['y'] = _G_apply_605
                _G_python_606, lastError = eval('t.Same(x, y)', self.globals, _locals), None
                return (_G_python_606, self.currentError)
            def _G_or_607():
                _G_python_608, lastError = '!=', None
                _G_apply_609, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_608])
                _G_apply_610, lastError = self._apply(self.rule_order, "order", [])
                _locals['y'] = _G_apply_610
                _G_python_611, lastError = eval('t.NotSame(x, y)', self.globals, _locals), None
                return (_G_python_611, self.currentError)
            def _G_or_612():
                _G_python_613, lastError = '&!', None
                _G_apply_614, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_613])
                _G_apply_615, lastError = self._apply(self.rule_order, "order", [])
                _locals['y'] = _G_apply_615
                _G_python_616, lastError = eval('t.ButNot(x, y)', self.globals, _locals), None
                return (_G_python_616, self.currentError)
            def _G_or_617():
                _G_python_618, lastError = '^', None
                _G_apply_619, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_618])
                _G_apply_620, lastError = self._apply(self.rule_order, "order", [])
                _locals['y'] = _G_apply_620
                _G_python_621, lastError = eval('t.BinaryXor(x, y)', self.globals, _locals), None
                return (_G_python_621, self.currentError)
            def _G_or_622():
                _G_python_623, lastError = eval('x', self.globals, _locals), None
                return (_G_python_623, self.currentError)
            _G_or_624, lastError = self._or([_G_or_592, _G_or_597, _G_or_602, _G_or_607, _G_or_612, _G_or_617, _G_or_622])
            return (_G_or_624, self.currentError)
        _G_or_625, lastError = self._or([_G_or_586, _G_or_588, _G_or_590])
        return (_G_or_625, self.currentError)


    def rule_band(self):
        _locals = {'self': self}
        self.locals['band'] = _locals
        def _G_or_626():
            _G_apply_627, lastError = self._apply(self.rule_band, "band", [])
            _locals['x'] = _G_apply_627
            def _G_not_628():
                def _G_or_629():
                    _G_python_630, lastError = '&&', None
                    _G_apply_631, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_630])
                    return (_G_apply_631, self.currentError)
                def _G_or_632():
                    _G_python_633, lastError = '&!', None
                    _G_apply_634, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_633])
                    return (_G_apply_634, self.currentError)
                _G_or_635, lastError = self._or([_G_or_629, _G_or_632])
                return (_G_or_635, self.currentError)
            _G_not_636, lastError = self._not(_G_not_628)
            _G_python_637, lastError = '&', None
            _G_apply_638, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_637])
            _G_apply_639, lastError = self._apply(self.rule_order, "order", [])
            _locals['y'] = _G_apply_639
            _G_python_640, lastError = eval('t.BinaryAnd(x, y)', self.globals, _locals), None
            return (_G_python_640, self.currentError)
        def _G_or_641():
            _G_apply_642, lastError = self._apply(self.rule_order, "order", [])
            _locals['x'] = _G_apply_642
            def _G_not_643():
                def _G_or_644():
                    _G_python_645, lastError = '&&', None
                    _G_apply_646, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_645])
                    return (_G_apply_646, self.currentError)
                def _G_or_647():
                    _G_python_648, lastError = '&!', None
                    _G_apply_649, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_648])
                    return (_G_apply_649, self.currentError)
                _G_or_650, lastError = self._or([_G_or_644, _G_or_647])
                return (_G_or_650, self.currentError)
            _G_not_651, lastError = self._not(_G_not_643)
            _G_python_652, lastError = '&', None
            _G_apply_653, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_652])
            _G_apply_654, lastError = self._apply(self.rule_order, "order", [])
            _locals['y'] = _G_apply_654
            _G_python_655, lastError = eval('t.BinaryAnd(x, y)', self.globals, _locals), None
            return (_G_python_655, self.currentError)
        _G_or_656, lastError = self._or([_G_or_626, _G_or_641])
        return (_G_or_656, self.currentError)


    def rule_bor(self):
        _locals = {'self': self}
        self.locals['bor'] = _locals
        def _G_or_657():
            _G_apply_658, lastError = self._apply(self.rule_bor, "bor", [])
            _locals['x'] = _G_apply_658
            _G_python_659, lastError = '|', None
            _G_apply_660, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_659])
            _G_apply_661, lastError = self._apply(self.rule_order, "order", [])
            _locals['y'] = _G_apply_661
            _G_python_662, lastError = eval('t.BinaryOr(x, y)', self.globals, _locals), None
            return (_G_python_662, self.currentError)
        def _G_or_663():
            _G_apply_664, lastError = self._apply(self.rule_order, "order", [])
            _locals['x'] = _G_apply_664
            _G_python_665, lastError = '|', None
            _G_apply_666, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_665])
            _G_apply_667, lastError = self._apply(self.rule_order, "order", [])
            _locals['y'] = _G_apply_667
            _G_python_668, lastError = eval('t.BinaryOr(x, y)', self.globals, _locals), None
            return (_G_python_668, self.currentError)
        _G_or_669, lastError = self._or([_G_or_657, _G_or_663])
        return (_G_or_669, self.currentError)


    def rule_condAnd(self):
        _locals = {'self': self}
        self.locals['condAnd'] = _locals
        _G_apply_670, lastError = self._apply(self.rule_logical, "logical", [])
        _locals['x'] = _G_apply_670
        def _G_or_671():
            _G_python_672, lastError = '&&', None
            _G_apply_673, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_672])
            _G_apply_674, lastError = self._apply(self.rule_condAnd, "condAnd", [])
            _locals['y'] = _G_apply_674
            _G_python_675, lastError = eval('t.LogicalAnd(x, y)', self.globals, _locals), None
            return (_G_python_675, self.currentError)
        def _G_or_676():
            _G_python_677, lastError = eval('x', self.globals, _locals), None
            return (_G_python_677, self.currentError)
        _G_or_678, lastError = self._or([_G_or_671, _G_or_676])
        return (_G_or_678, self.currentError)


    def rule_cond(self):
        _locals = {'self': self}
        self.locals['cond'] = _locals
        _G_apply_679, lastError = self._apply(self.rule_condAnd, "condAnd", [])
        _locals['x'] = _G_apply_679
        def _G_or_680():
            _G_python_681, lastError = '||', None
            _G_apply_682, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_681])
            _G_apply_683, lastError = self._apply(self.rule_cond, "cond", [])
            _locals['y'] = _G_apply_683
            _G_python_684, lastError = eval('t.LogicalOr(x, y)', self.globals, _locals), None
            return (_G_python_684, self.currentError)
        def _G_or_685():
            _G_python_686, lastError = eval('x', self.globals, _locals), None
            return (_G_python_686, self.currentError)
        _G_or_687, lastError = self._or([_G_or_680, _G_or_685])
        return (_G_or_687, self.currentError)


    def rule_assign(self):
        _locals = {'self': self}
        self.locals['assign'] = _locals
        def _G_or_688():
            def _G_not_689():
                _G_apply_690, lastError = self._apply(self.rule_objectExpr, "objectExpr", [])
                return (_G_apply_690, self.currentError)
            _G_not_691, lastError = self._not(_G_not_689)
            _G_python_692, lastError = 'def', None
            _G_apply_693, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_692])
            def _G_or_694():
                _G_apply_695, lastError = self._apply(self.rule_pattern, "pattern", [])
                _locals['p'] = _G_apply_695
                def _G_optional_696():
                    _G_python_697, lastError = 'exit', None
                    _G_apply_698, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_697])
                    _G_apply_699, lastError = self._apply(self.rule_order, "order", [])
                    return (_G_apply_699, self.currentError)
                def _G_optional_700():
                    return (None, self.input.nullError())
                _G_or_701, lastError = self._or([_G_optional_696, _G_optional_700])
                _locals['e'] = _G_or_701
                _G_python_702, lastError = ':=', None
                _G_apply_703, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_702])
                _G_apply_704, lastError = self._apply(self.rule_assign, "assign", [])
                _locals['a'] = _G_apply_704
                _G_python_705, lastError = eval('t.Def(p, e, a)', self.globals, _locals), None
                return (_G_python_705, self.currentError)
            def _G_or_706():
                _G_apply_707, lastError = self._apply(self.rule_noun, "noun", [])
                _locals['n'] = _G_apply_707
                def _G_or_708():
                    def _G_lookahead_709():
                        _G_apply_710, lastError = self._apply(self.rule_seqSep, "seqSep", [])
                        return (_G_apply_710, self.currentError)
                    _G_lookahead_711, lastError = self.lookahead(_G_lookahead_709)
                    return (_G_lookahead_711, self.currentError)
                def _G_or_712():
                    _G_apply_713, lastError = self._apply(self.rule_end, "end", [])
                    return (_G_apply_713, self.currentError)
                _G_or_714, lastError = self._or([_G_or_708, _G_or_712])
                _G_python_715, lastError = eval('t.Forward(n)', self.globals, _locals), None
                return (_G_python_715, self.currentError)
            _G_or_716, lastError = self._or([_G_or_694, _G_or_706])
            return (_G_or_716, self.currentError)
        def _G_or_717():
            _G_apply_718, lastError = self._apply(self.rule_keywordPattern, "keywordPattern", [])
            _locals['p'] = _G_apply_718
            _G_python_719, lastError = ':=', None
            _G_apply_720, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_719])
            _G_apply_721, lastError = self._apply(self.rule_assign, "assign", [])
            _locals['a'] = _G_apply_721
            _G_python_722, lastError = eval('t.Def(p, None, a)', self.globals, _locals), None
            return (_G_python_722, self.currentError)
        def _G_or_723():
            _G_apply_724, lastError = self._apply(self.rule_cond, "cond", [])
            _locals['x'] = _G_apply_724
            def _G_or_725():
                _G_python_726, lastError = ':=', None
                _G_apply_727, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_726])
                _G_apply_728, lastError = self._apply(self.rule_assign, "assign", [])
                _locals['y'] = _G_apply_728
                _G_python_729, lastError = eval('t.Assign(x, y)', self.globals, _locals), None
                return (_G_python_729, self.currentError)
            def _G_or_730():
                _G_apply_731, lastError = self._apply(self.rule_assignOp, "assignOp", [])
                _locals['o'] = _G_apply_731
                _G_apply_732, lastError = self._apply(self.rule_assign, "assign", [])
                _locals['y'] = _G_apply_732
                _G_python_733, lastError = eval('t.AugAssign(o, x, y)', self.globals, _locals), None
                return (_G_python_733, self.currentError)
            def _G_or_734():
                _G_apply_735, lastError = self._apply(self.rule_identifier, "identifier", [])
                _locals['v'] = _G_apply_735
                _G_exactly_736, lastError = self.exactly('=')
                def _G_or_737():
                    _G_apply_738, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
                    _locals['y'] = _G_apply_738
                    _G_python_739, lastError = eval('t.VerbAssign(v, x, y)', self.globals, _locals), None
                    return (_G_python_739, self.currentError)
                def _G_or_740():
                    _G_apply_741, lastError = self._apply(self.rule_assign, "assign", [])
                    _locals['y'] = _G_apply_741
                    _G_python_742, lastError = eval('t.VerbAssign(v, x, [y])', self.globals, _locals), None
                    return (_G_python_742, self.currentError)
                _G_or_743, lastError = self._or([_G_or_737, _G_or_740])
                return (_G_or_743, self.currentError)
            def _G_or_744():
                _G_python_745, lastError = eval('x', self.globals, _locals), None
                return (_G_python_745, self.currentError)
            _G_or_746, lastError = self._or([_G_or_725, _G_or_730, _G_or_734, _G_or_744])
            return (_G_or_746, self.currentError)
        _G_or_747, lastError = self._or([_G_or_688, _G_or_717, _G_or_723])
        return (_G_or_747, self.currentError)


    def rule_assignOp(self):
        _locals = {'self': self}
        self.locals['assignOp'] = _locals
        def _G_or_748():
            _G_python_749, lastError = '+=', None
            _G_apply_750, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_749])
            _G_python_751, lastError = "Add", None
            return (_G_python_751, self.currentError)
        def _G_or_752():
            _G_python_753, lastError = '-=', None
            _G_apply_754, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_753])
            _G_python_755, lastError = "Subtract", None
            return (_G_python_755, self.currentError)
        def _G_or_756():
            _G_python_757, lastError = '*=', None
            _G_apply_758, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_757])
            _G_python_759, lastError = "Multiply", None
            return (_G_python_759, self.currentError)
        def _G_or_760():
            _G_python_761, lastError = '/=', None
            _G_apply_762, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_761])
            _G_python_763, lastError = "Divide", None
            return (_G_python_763, self.currentError)
        def _G_or_764():
            _G_python_765, lastError = '%=', None
            _G_apply_766, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_765])
            _G_python_767, lastError = "Remainder", None
            return (_G_python_767, self.currentError)
        def _G_or_768():
            _G_python_769, lastError = '%%=', None
            _G_apply_770, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_769])
            _G_python_771, lastError = "Mod", None
            return (_G_python_771, self.currentError)
        def _G_or_772():
            _G_python_773, lastError = '**=', None
            _G_apply_774, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_773])
            _G_python_775, lastError = "Pow", None
            return (_G_python_775, self.currentError)
        def _G_or_776():
            _G_python_777, lastError = '//=', None
            _G_apply_778, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_777])
            _G_python_779, lastError = "FloorDivide", None
            return (_G_python_779, self.currentError)
        def _G_or_780():
            _G_python_781, lastError = '>>=', None
            _G_apply_782, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_781])
            _G_python_783, lastError = "ShiftRight", None
            return (_G_python_783, self.currentError)
        def _G_or_784():
            _G_python_785, lastError = '<<=', None
            _G_apply_786, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_785])
            _G_python_787, lastError = "ShiftLeft", None
            return (_G_python_787, self.currentError)
        def _G_or_788():
            _G_python_789, lastError = '&=', None
            _G_apply_790, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_789])
            _G_python_791, lastError = "BinaryAnd", None
            return (_G_python_791, self.currentError)
        def _G_or_792():
            _G_python_793, lastError = '|=', None
            _G_apply_794, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_793])
            _G_python_795, lastError = "BinaryOr", None
            return (_G_python_795, self.currentError)
        def _G_or_796():
            _G_python_797, lastError = '^=', None
            _G_apply_798, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_797])
            _G_python_799, lastError = "BinaryXor", None
            return (_G_python_799, self.currentError)
        _G_or_800, lastError = self._or([_G_or_748, _G_or_752, _G_or_756, _G_or_760, _G_or_764, _G_or_768, _G_or_772, _G_or_776, _G_or_780, _G_or_784, _G_or_788, _G_or_792, _G_or_796])
        return (_G_or_800, self.currentError)


    def rule_expr(self):
        _locals = {'self': self}
        self.locals['expr'] = _locals
        def _G_or_801():
            _G_apply_802, lastError = self._apply(self.rule_assign, "assign", [])
            return (_G_apply_802, self.currentError)
        def _G_or_803():
            _G_apply_804, lastError = self._apply(self.rule_ejector, "ejector", [])
            return (_G_apply_804, self.currentError)
        _G_or_805, lastError = self._or([_G_or_801, _G_or_803])
        return (_G_or_805, self.currentError)


    def rule_ejector(self):
        _locals = {'self': self}
        self.locals['ejector'] = _locals
        def _G_or_806():
            _G_python_807, lastError = "break", None
            _G_apply_808, lastError = self._apply(self.rule_token, "token", [_G_python_807])
            _G_python_809, lastError = eval('t.Break', self.globals, _locals), None
            return (_G_python_809, self.currentError)
        def _G_or_810():
            _G_python_811, lastError = "continue", None
            _G_apply_812, lastError = self._apply(self.rule_token, "token", [_G_python_811])
            _G_python_813, lastError = eval('t.Continue', self.globals, _locals), None
            return (_G_python_813, self.currentError)
        def _G_or_814():
            _G_python_815, lastError = "return", None
            _G_apply_816, lastError = self._apply(self.rule_token, "token", [_G_python_815])
            _G_python_817, lastError = eval('t.Return', self.globals, _locals), None
            return (_G_python_817, self.currentError)
        _G_or_818, lastError = self._or([_G_or_806, _G_or_810, _G_or_814])
        _locals['ej'] = _G_or_818
        def _G_optional_819():
            def _G_or_820():
                _G_python_821, lastError = '(', None
                _G_apply_822, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_821])
                _G_python_823, lastError = ")", None
                _G_apply_824, lastError = self._apply(self.rule_token, "token", [_G_python_823])
                _G_python_825, lastError = None, None
                return (_G_python_825, self.currentError)
            def _G_or_826():
                _G_apply_827, lastError = self._apply(self.rule_assign, "assign", [])
                return (_G_apply_827, self.currentError)
            _G_or_828, lastError = self._or([_G_or_820, _G_or_826])
            return (_G_or_828, self.currentError)
        def _G_optional_829():
            return (None, self.input.nullError())
        _G_or_830, lastError = self._or([_G_optional_819, _G_optional_829])
        _locals['val'] = _G_or_830
        _G_python_831, lastError = eval('ej(val)', self.globals, _locals), None
        return (_G_python_831, self.currentError)


    def rule_guard(self):
        _locals = {'self': self}
        self.locals['guard'] = _locals
        def _G_or_832():
            _G_apply_833, lastError = self._apply(self.rule_noun, "noun", [])
            return (_G_apply_833, self.currentError)
        def _G_or_834():
            _G_apply_835, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
            return (_G_apply_835, self.currentError)
        _G_or_836, lastError = self._or([_G_or_832, _G_or_834])
        _locals['e'] = _G_or_836
        def _G_many_837():
            _G_python_838, lastError = '[', None
            _G_apply_839, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_838])
            _G_apply_840, lastError = self._apply(self.rule_args, "args", [])
            _locals['x'] = _G_apply_840
            _G_python_841, lastError = ']', None
            _G_apply_842, lastError = self._apply(self.rule_token, "token", [_G_python_841])
            _G_python_843, lastError = eval('x', self.globals, _locals), None
            return (_G_python_843, self.currentError)
        _G_many_844, lastError = self.many(_G_many_837)
        _locals['xs'] = _G_many_844
        _G_python_845, lastError = eval('t.Guard(e, xs)', self.globals, _locals), None
        return (_G_python_845, self.currentError)


    def rule_optGuard(self):
        _locals = {'self': self}
        self.locals['optGuard'] = _locals
        def _G_optional_846():
            _G_python_847, lastError = ':', None
            _G_apply_848, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_847])
            _G_apply_849, lastError = self._apply(self.rule_guard, "guard", [])
            return (_G_apply_849, self.currentError)
        def _G_optional_850():
            return (None, self.input.nullError())
        _G_or_851, lastError = self._or([_G_optional_846, _G_optional_850])
        return (_G_or_851, self.currentError)


    def rule_eqPattern(self):
        _locals = {'self': self}
        self.locals['eqPattern'] = _locals
        def _G_or_852():
            _G_python_853, lastError = '_', None
            _G_apply_854, lastError = self._apply(self.rule_token, "token", [_G_python_853])
            def _G_not_855():
                _G_apply_856, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                return (_G_apply_856, self.currentError)
            _G_not_857, lastError = self._not(_G_not_855)
            _G_apply_858, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['e'] = _G_apply_858
            _G_python_859, lastError = eval('t.IgnorePattern(e)', self.globals, _locals), None
            return (_G_python_859, self.currentError)
        def _G_or_860():
            def _G_optional_861():
                _G_apply_862, lastError = self._apply(self.rule_identifier, "identifier", [])
                return (_G_apply_862, self.currentError)
            def _G_optional_863():
                return (None, self.input.nullError())
            _G_or_864, lastError = self._or([_G_optional_861, _G_optional_863])
            _locals['n'] = _G_or_864
            _G_apply_865, lastError = self._apply(self.rule_quasiString, "quasiString", [])
            _locals['q'] = _G_apply_865
            _G_python_866, lastError = eval('t.QuasiPattern(n, q)', self.globals, _locals), None
            return (_G_python_866, self.currentError)
        def _G_or_867():
            _G_apply_868, lastError = self._apply(self.rule_namePattern, "namePattern", [])
            return (_G_apply_868, self.currentError)
        def _G_or_869():
            _G_python_870, lastError = '==', None
            _G_apply_871, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_870])
            _G_apply_872, lastError = self._apply(self.rule_prim, "prim", [])
            _locals['p'] = _G_apply_872
            _G_python_873, lastError = eval('t.SamePattern(p)', self.globals, _locals), None
            return (_G_python_873, self.currentError)
        def _G_or_874():
            _G_python_875, lastError = '!=', None
            _G_apply_876, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_875])
            _G_apply_877, lastError = self._apply(self.rule_prim, "prim", [])
            _locals['p'] = _G_apply_877
            _G_python_878, lastError = eval('throwSemanticHere("reserved: not-same pattern")', self.globals, _locals), None
            return (_G_python_878, self.currentError)
        _G_or_879, lastError = self._or([_G_or_852, _G_or_860, _G_or_867, _G_or_869, _G_or_874])
        return (_G_or_879, self.currentError)


    def rule_patterns(self):
        _locals = {'self': self}
        self.locals['patterns'] = _locals
        def _G_or_880():
            _G_apply_881, lastError = self._apply(self.rule_pattern, "pattern", [])
            _locals['p'] = _G_apply_881
            def _G_many_882():
                _G_python_883, lastError = ',', None
                _G_apply_884, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_883])
                _G_apply_885, lastError = self._apply(self.rule_pattern, "pattern", [])
                return (_G_apply_885, self.currentError)
            _G_many_886, lastError = self.many(_G_many_882)
            _locals['ps'] = _G_many_886
            _G_python_887, lastError = eval('[p] + ps', self.globals, _locals), None
            return (_G_python_887, self.currentError)
        def _G_or_888():
            _G_python_889, lastError = [], None
            return (_G_python_889, self.currentError)
        _G_or_890, lastError = self._or([_G_or_880, _G_or_888])
        return (_G_or_890, self.currentError)


    def rule_key(self):
        _locals = {'self': self}
        self.locals['key'] = _locals
        def _G_or_891():
            _G_apply_892, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
            return (_G_apply_892, self.currentError)
        def _G_or_893():
            _G_apply_894, lastError = self._apply(self.rule_literal, "literal", [])
            return (_G_apply_894, self.currentError)
        _G_or_895, lastError = self._or([_G_or_891, _G_or_893])
        _locals['x'] = _G_or_895
        _G_apply_896, lastError = self._apply(self.rule_br, "br", [])
        _G_python_897, lastError = eval('x', self.globals, _locals), None
        return (_G_python_897, self.currentError)


    def rule_keywordPattern(self):
        _locals = {'self': self}
        self.locals['keywordPattern'] = _locals
        def _G_or_898():
            _G_python_899, lastError = "var", None
            _G_apply_900, lastError = self._apply(self.rule_token, "token", [_G_python_899])
            _G_apply_901, lastError = self._apply(self.rule_noun, "noun", [])
            _locals['n'] = _G_apply_901
            _G_apply_902, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['g'] = _G_apply_902
            _G_python_903, lastError = eval('t.VarPattern(n, g)', self.globals, _locals), None
            return (_G_python_903, self.currentError)
        def _G_or_904():
            _G_python_905, lastError = "bind", None
            _G_apply_906, lastError = self._apply(self.rule_token, "token", [_G_python_905])
            _G_apply_907, lastError = self._apply(self.rule_noun, "noun", [])
            _locals['n'] = _G_apply_907
            _G_apply_908, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['g'] = _G_apply_908
            _G_python_909, lastError = eval('t.BindPattern(n, g)', self.globals, _locals), None
            return (_G_python_909, self.currentError)
        _G_or_910, lastError = self._or([_G_or_898, _G_or_904])
        return (_G_or_910, self.currentError)


    def rule_namePattern(self):
        _locals = {'self': self}
        self.locals['namePattern'] = _locals
        def _G_or_911():
            _G_apply_912, lastError = self._apply(self.rule_keywordPattern, "keywordPattern", [])
            return (_G_apply_912, self.currentError)
        def _G_or_913():
            _G_apply_914, lastError = self._apply(self.rule_noun, "noun", [])
            _locals['n'] = _G_apply_914
            _G_apply_915, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['g'] = _G_apply_915
            _G_python_916, lastError = eval('t.FinalPattern(n, g)', self.globals, _locals), None
            return (_G_python_916, self.currentError)
        def _G_or_917():
            _G_apply_918, lastError = self._apply(self.rule_reifyPattern, "reifyPattern", [])
            return (_G_apply_918, self.currentError)
        _G_or_919, lastError = self._or([_G_or_911, _G_or_913, _G_or_917])
        return (_G_or_919, self.currentError)


    def rule_reifyPattern(self):
        _locals = {'self': self}
        self.locals['reifyPattern'] = _locals
        def _G_or_920():
            _G_python_921, lastError = '&&', None
            _G_apply_922, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_921])
            _G_apply_923, lastError = self._apply(self.rule_noun, "noun", [])
            _locals['n'] = _G_apply_923
            _G_apply_924, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['g'] = _G_apply_924
            _G_python_925, lastError = eval('t.BindingPattern(n, g)', self.globals, _locals), None
            return (_G_python_925, self.currentError)
        def _G_or_926():
            _G_python_927, lastError = '&', None
            _G_apply_928, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_927])
            _G_apply_929, lastError = self._apply(self.rule_noun, "noun", [])
            _locals['n'] = _G_apply_929
            _G_apply_930, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['g'] = _G_apply_930
            _G_python_931, lastError = eval('t.SlotPattern(n, g)', self.globals, _locals), None
            return (_G_python_931, self.currentError)
        _G_or_932, lastError = self._or([_G_or_920, _G_or_926])
        return (_G_or_932, self.currentError)


    def rule_mapPatternAddressing(self):
        _locals = {'self': self}
        self.locals['mapPatternAddressing'] = _locals
        def _G_or_933():
            _G_apply_934, lastError = self._apply(self.rule_key, "key", [])
            _locals['k'] = _G_apply_934
            _G_python_935, lastError = '=>', None
            _G_apply_936, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_935])
            _G_apply_937, lastError = self._apply(self.rule_pattern, "pattern", [])
            _locals['v'] = _G_apply_937
            _G_python_938, lastError = eval('t.MapPatternAssoc(k, v)', self.globals, _locals), None
            return (_G_python_938, self.currentError)
        def _G_or_939():
            _G_python_940, lastError = '=>', None
            _G_apply_941, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_940])
            _G_apply_942, lastError = self._apply(self.rule_namePattern, "namePattern", [])
            _locals['p'] = _G_apply_942
            _G_python_943, lastError = eval('t.MapPatternImport(p)', self.globals, _locals), None
            return (_G_python_943, self.currentError)
        _G_or_944, lastError = self._or([_G_or_933, _G_or_939])
        return (_G_or_944, self.currentError)


    def rule_mapPattern(self):
        _locals = {'self': self}
        self.locals['mapPattern'] = _locals
        _G_apply_945, lastError = self._apply(self.rule_mapPatternAddressing, "mapPatternAddressing", [])
        _locals['a'] = _G_apply_945
        def _G_or_946():
            _G_python_947, lastError = ':=', None
            _G_apply_948, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_947])
            _G_apply_949, lastError = self._apply(self.rule_order, "order", [])
            _locals['d'] = _G_apply_949
            _G_python_950, lastError = eval('t.MapPatternOptional(a, d)', self.globals, _locals), None
            return (_G_python_950, self.currentError)
        def _G_or_951():
            _G_python_952, lastError = eval('t.MapPatternRequired(a)', self.globals, _locals), None
            return (_G_python_952, self.currentError)
        _G_or_953, lastError = self._or([_G_or_946, _G_or_951])
        return (_G_or_953, self.currentError)


    def rule_mapPatts(self):
        _locals = {'self': self}
        self.locals['mapPatts'] = _locals
        _G_apply_954, lastError = self._apply(self.rule_mapPattern, "mapPattern", [])
        _locals['m'] = _G_apply_954
        def _G_many_955():
            _G_python_956, lastError = ',', None
            _G_apply_957, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_956])
            _G_apply_958, lastError = self._apply(self.rule_mapPattern, "mapPattern", [])
            return (_G_apply_958, self.currentError)
        _G_many_959, lastError = self.many(_G_many_955)
        _locals['ms'] = _G_many_959
        _G_python_960, lastError = eval('[m] + ms', self.globals, _locals), None
        return (_G_python_960, self.currentError)


    def rule_listPatternInner(self):
        _locals = {'self': self}
        self.locals['listPatternInner'] = _locals
        def _G_or_961():
            _G_apply_962, lastError = self._apply(self.rule_mapPatts, "mapPatts", [])
            _locals['ms'] = _G_apply_962
            _G_apply_963, lastError = self._apply(self.rule_br, "br", [])
            _G_python_964, lastError = ']', None
            _G_apply_965, lastError = self._apply(self.rule_token, "token", [_G_python_964])
            def _G_optional_966():
                _G_python_967, lastError = '|', None
                _G_apply_968, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_967])
                _G_apply_969, lastError = self._apply(self.rule_listPattern, "listPattern", [])
                return (_G_apply_969, self.currentError)
            def _G_optional_970():
                return (None, self.input.nullError())
            _G_or_971, lastError = self._or([_G_optional_966, _G_optional_970])
            _locals['tail'] = _G_or_971
            _G_python_972, lastError = eval('t.MapPattern(ms, tail)', self.globals, _locals), None
            return (_G_python_972, self.currentError)
        def _G_or_973():
            _G_apply_974, lastError = self._apply(self.rule_patterns, "patterns", [])
            _locals['ps'] = _G_apply_974
            _G_apply_975, lastError = self._apply(self.rule_br, "br", [])
            _G_python_976, lastError = ']', None
            _G_apply_977, lastError = self._apply(self.rule_token, "token", [_G_python_976])
            def _G_optional_978():
                _G_python_979, lastError = '+', None
                _G_apply_980, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_979])
                _G_apply_981, lastError = self._apply(self.rule_listPattern, "listPattern", [])
                return (_G_apply_981, self.currentError)
            def _G_optional_982():
                return (None, self.input.nullError())
            _G_or_983, lastError = self._or([_G_optional_978, _G_optional_982])
            _locals['tail'] = _G_or_983
            _G_python_984, lastError = eval('t.ListPattern(ps, tail)', self.globals, _locals), None
            return (_G_python_984, self.currentError)
        _G_or_985, lastError = self._or([_G_or_961, _G_or_973])
        return (_G_or_985, self.currentError)


    def rule_listPattern(self):
        _locals = {'self': self}
        self.locals['listPattern'] = _locals
        def _G_or_986():
            _G_python_987, lastError = 'via', None
            _G_apply_988, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_987])
            _G_apply_989, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
            _locals['e'] = _G_apply_989
            _G_apply_990, lastError = self._apply(self.rule_listPattern, "listPattern", [])
            _locals['p'] = _G_apply_990
            _G_python_991, lastError = eval('t.ViaPattern(e, p)', self.globals, _locals), None
            return (_G_python_991, self.currentError)
        def _G_or_992():
            _G_apply_993, lastError = self._apply(self.rule_eqPattern, "eqPattern", [])
            return (_G_apply_993, self.currentError)
        def _G_or_994():
            _G_python_995, lastError = '[', None
            _G_apply_996, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_995])
            _G_apply_997, lastError = self._apply(self.rule_listPatternInner, "listPatternInner", [])
            return (_G_apply_997, self.currentError)
        _G_or_998, lastError = self._or([_G_or_986, _G_or_992, _G_or_994])
        return (_G_or_998, self.currentError)


    def rule_pattern(self):
        _locals = {'self': self}
        self.locals['pattern'] = _locals
        _G_apply_999, lastError = self._apply(self.rule_listPattern, "listPattern", [])
        _locals['p'] = _G_apply_999
        def _G_or_1000():
            _G_python_1001, lastError = '?', None
            _G_apply_1002, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1001])
            _G_apply_1003, lastError = self._apply(self.rule_order, "order", [])
            _locals['e'] = _G_apply_1003
            _G_python_1004, lastError = eval('t.SuchThatPattern(p, e)', self.globals, _locals), None
            return (_G_python_1004, self.currentError)
        def _G_or_1005():
            _G_python_1006, lastError = eval('p', self.globals, _locals), None
            return (_G_python_1006, self.currentError)
        _G_or_1007, lastError = self._or([_G_or_1000, _G_or_1005])
        return (_G_or_1007, self.currentError)


    def rule_basic(self):
        _locals = {'self': self}
        self.locals['basic'] = _locals
        def _G_or_1008():
            _G_apply_1009, lastError = self._apply(self.rule_docoDef, "docoDef", [])
            return (_G_apply_1009, self.currentError)
        def _G_or_1010():
            _G_apply_1011, lastError = self._apply(self.rule_accumExpr, "accumExpr", [])
            return (_G_apply_1011, self.currentError)
        def _G_or_1012():
            _G_apply_1013, lastError = self._apply(self.rule_escapeExpr, "escapeExpr", [])
            return (_G_apply_1013, self.currentError)
        def _G_or_1014():
            _G_apply_1015, lastError = self._apply(self.rule_forExpr, "forExpr", [])
            return (_G_apply_1015, self.currentError)
        def _G_or_1016():
            _G_apply_1017, lastError = self._apply(self.rule_ifExpr, "ifExpr", [])
            return (_G_apply_1017, self.currentError)
        def _G_or_1018():
            _G_apply_1019, lastError = self._apply(self.rule_lambdaExpr, "lambdaExpr", [])
            return (_G_apply_1019, self.currentError)
        def _G_or_1020():
            _G_apply_1021, lastError = self._apply(self.rule_metaExpr, "metaExpr", [])
            return (_G_apply_1021, self.currentError)
        def _G_or_1022():
            _G_apply_1023, lastError = self._apply(self.rule_switchExpr, "switchExpr", [])
            return (_G_apply_1023, self.currentError)
        def _G_or_1024():
            _G_apply_1025, lastError = self._apply(self.rule_tryExpr, "tryExpr", [])
            return (_G_apply_1025, self.currentError)
        def _G_or_1026():
            _G_apply_1027, lastError = self._apply(self.rule_whileExpr, "whileExpr", [])
            return (_G_apply_1027, self.currentError)
        def _G_or_1028():
            _G_apply_1029, lastError = self._apply(self.rule_whenExpr, "whenExpr", [])
            return (_G_apply_1029, self.currentError)
        _G_or_1030, lastError = self._or([_G_or_1008, _G_or_1010, _G_or_1012, _G_or_1014, _G_or_1016, _G_or_1018, _G_or_1020, _G_or_1022, _G_or_1024, _G_or_1026, _G_or_1028])
        return (_G_or_1030, self.currentError)


    def rule_docoDef(self):
        _locals = {'self': self}
        self.locals['docoDef'] = _locals
        def _G_optional_1031():
            _G_apply_1032, lastError = self._apply(self.rule_doco, "doco", [])
            return (_G_apply_1032, self.currentError)
        def _G_optional_1033():
            return (None, self.input.nullError())
        _G_or_1034, lastError = self._or([_G_optional_1031, _G_optional_1033])
        _locals['doc'] = _G_or_1034
        def _G_or_1035():
            _G_apply_1036, lastError = self._apply(self.rule_objectExpr, "objectExpr", [])
            _locals['o'] = _G_apply_1036
            _G_python_1037, lastError = eval('t.Object(doc, *o)', self.globals, _locals), None
            return (_G_python_1037, self.currentError)
        def _G_or_1038():
            _G_apply_1039, lastError = self._apply(self.rule_interfaceExpr, "interfaceExpr", [])
            _locals['i'] = _G_apply_1039
            _G_python_1040, lastError = eval('t.Interface(doc, *i)', self.globals, _locals), None
            return (_G_python_1040, self.currentError)
        _G_or_1041, lastError = self._or([_G_or_1035, _G_or_1038])
        return (_G_or_1041, self.currentError)


    def rule_doco(self):
        _locals = {'self': self}
        self.locals['doco'] = _locals
        _G_python_1042, lastError = "/**", None
        _G_apply_1043, lastError = self._apply(self.rule_token, "token", [_G_python_1042])
        def _G_consumedby_1044():
            def _G_many_1045():
                def _G_not_1046():
                    _G_exactly_1047, lastError = self.exactly('*')
                    _G_exactly_1048, lastError = self.exactly('/')
                    return (_G_exactly_1048, self.currentError)
                _G_not_1049, lastError = self._not(_G_not_1046)
                _G_apply_1050, lastError = self._apply(self.rule_anything, "anything", [])
                return (_G_apply_1050, self.currentError)
            _G_many_1051, lastError = self.many(_G_many_1045)
            return (_G_many_1051, self.currentError)
        _G_consumedby_1052, lastError = self.consumedby(_G_consumedby_1044)
        _locals['doc'] = _G_consumedby_1052
        _G_exactly_1053, lastError = self.exactly('*')
        _G_exactly_1054, lastError = self.exactly('/')
        _G_python_1055, lastError = eval('doc.strip()', self.globals, _locals), None
        return (_G_python_1055, self.currentError)


    def rule_objectExpr(self):
        _locals = {'self': self}
        self.locals['objectExpr'] = _locals
        def _G_or_1056():
            _G_python_1057, lastError = "def", None
            _G_apply_1058, lastError = self._apply(self.rule_token, "token", [_G_python_1057])
            _G_apply_1059, lastError = self._apply(self.rule_objectName, "objectName", [])
            _locals['n'] = _G_apply_1059
            return (_locals['n'], self.currentError)
        def _G_or_1060():
            _G_apply_1061, lastError = self._apply(self.rule_keywordPattern, "keywordPattern", [])
            _locals['n'] = _G_apply_1061
            return (_locals['n'], self.currentError)
        _G_or_1062, lastError = self._or([_G_or_1056, _G_or_1060])
        _G_apply_1063, lastError = self._apply(self.rule_objectTail, "objectTail", [])
        _locals['tail'] = _G_apply_1063
        _G_python_1064, lastError = eval('[n, tail]', self.globals, _locals), None
        return (_G_python_1064, self.currentError)


    def rule_objectName(self):
        _locals = {'self': self}
        self.locals['objectName'] = _locals
        def _G_or_1065():
            _G_python_1066, lastError = '_', None
            _G_apply_1067, lastError = self._apply(self.rule_token, "token", [_G_python_1066])
            _G_apply_1068, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['e'] = _G_apply_1068
            _G_python_1069, lastError = eval('t.IgnorePattern(e)', self.globals, _locals), None
            return (_G_python_1069, self.currentError)
        def _G_or_1070():
            _G_apply_1071, lastError = self._apply(self.rule_namePattern, "namePattern", [])
            return (_G_apply_1071, self.currentError)
        _G_or_1072, lastError = self._or([_G_or_1065, _G_or_1070])
        return (_G_or_1072, self.currentError)


    def rule_objectTail(self):
        _locals = {'self': self}
        self.locals['objectTail'] = _locals
        def _G_or_1073():
            _G_apply_1074, lastError = self._apply(self.rule_functionTail, "functionTail", [])
            return (_G_apply_1074, self.currentError)
        def _G_or_1075():
            def _G_optional_1076():
                _G_python_1077, lastError = "extends", None
                _G_apply_1078, lastError = self._apply(self.rule_token, "token", [_G_python_1077])
                _G_apply_1079, lastError = self._apply(self.rule_br, "br", [])
                _G_apply_1080, lastError = self._apply(self.rule_order, "order", [])
                return (_G_apply_1080, self.currentError)
            def _G_optional_1081():
                return (None, self.input.nullError())
            _G_or_1082, lastError = self._or([_G_optional_1076, _G_optional_1081])
            _locals['e'] = _G_or_1082
            def _G_optional_1083():
                _G_apply_1084, lastError = self._apply(self.rule_oAs, "oAs", [])
                return (_G_apply_1084, self.currentError)
            def _G_optional_1085():
                return (None, self.input.nullError())
            _G_or_1086, lastError = self._or([_G_optional_1083, _G_optional_1085])
            _locals['g'] = _G_or_1086
            _G_apply_1087, lastError = self._apply(self.rule_oImplements, "oImplements", [])
            _locals['oi'] = _G_apply_1087
            _G_apply_1088, lastError = self._apply(self.rule_scriptPair, "scriptPair", [])
            _locals['s'] = _G_apply_1088
            _G_python_1089, lastError = eval('t.Script(e, g, oi, *s)', self.globals, _locals), None
            return (_G_python_1089, self.currentError)
        _G_or_1090, lastError = self._or([_G_or_1073, _G_or_1075])
        return (_G_or_1090, self.currentError)


    def rule_oAs(self):
        _locals = {'self': self}
        self.locals['oAs'] = _locals
        _G_python_1091, lastError = "as", None
        _G_apply_1092, lastError = self._apply(self.rule_token, "token", [_G_python_1091])
        _G_apply_1093, lastError = self._apply(self.rule_br, "br", [])
        _G_apply_1094, lastError = self._apply(self.rule_order, "order", [])
        return (_G_apply_1094, self.currentError)


    def rule_oImplements(self):
        _locals = {'self': self}
        self.locals['oImplements'] = _locals
        def _G_or_1095():
            _G_python_1096, lastError = "implements", None
            _G_apply_1097, lastError = self._apply(self.rule_token, "token", [_G_python_1096])
            _G_apply_1098, lastError = self._apply(self.rule_br, "br", [])
            _G_apply_1099, lastError = self._apply(self.rule_order, "order", [])
            _locals['x'] = _G_apply_1099
            def _G_many_1100():
                _G_python_1101, lastError = ',', None
                _G_apply_1102, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1101])
                _G_apply_1103, lastError = self._apply(self.rule_order, "order", [])
                return (_G_apply_1103, self.currentError)
            _G_many_1104, lastError = self.many(_G_many_1100)
            _locals['xs'] = _G_many_1104
            _G_python_1105, lastError = eval('[x] + xs', self.globals, _locals), None
            return (_G_python_1105, self.currentError)
        def _G_or_1106():
            _G_python_1107, lastError = [], None
            return (_G_python_1107, self.currentError)
        _G_or_1108, lastError = self._or([_G_or_1095, _G_or_1106])
        return (_G_or_1108, self.currentError)


    def rule_functionTail(self):
        _locals = {'self': self}
        self.locals['functionTail'] = _locals
        _G_apply_1109, lastError = self._apply(self.rule_parenParamList, "parenParamList", [])
        _locals['ps'] = _G_apply_1109
        _G_apply_1110, lastError = self._apply(self.rule_optResultGuard, "optResultGuard", [])
        _locals['g'] = _G_apply_1110
        _G_apply_1111, lastError = self._apply(self.rule_oImplements, "oImplements", [])
        _locals['fi'] = _G_apply_1111
        _G_apply_1112, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1112
        _G_python_1113, lastError = eval('t.Function(ps, g, fi, b)', self.globals, _locals), None
        return (_G_python_1113, self.currentError)


    def rule_parenParamList(self):
        _locals = {'self': self}
        self.locals['parenParamList'] = _locals
        _G_python_1114, lastError = '(', None
        _G_apply_1115, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1114])
        def _G_or_1116():
            _G_apply_1117, lastError = self._apply(self.rule_pattern, "pattern", [])
            _locals['p'] = _G_apply_1117
            def _G_many_1118():
                _G_python_1119, lastError = ',', None
                _G_apply_1120, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1119])
                _G_apply_1121, lastError = self._apply(self.rule_pattern, "pattern", [])
                return (_G_apply_1121, self.currentError)
            _G_many_1122, lastError = self.many(_G_many_1118)
            _locals['ps'] = _G_many_1122
            _G_python_1123, lastError = ")", None
            _G_apply_1124, lastError = self._apply(self.rule_token, "token", [_G_python_1123])
            _G_python_1125, lastError = eval('[p] +  ps', self.globals, _locals), None
            return (_G_python_1125, self.currentError)
        def _G_or_1126():
            _G_python_1127, lastError = ")", None
            _G_apply_1128, lastError = self._apply(self.rule_token, "token", [_G_python_1127])
            _G_python_1129, lastError = [], None
            return (_G_python_1129, self.currentError)
        _G_or_1130, lastError = self._or([_G_or_1116, _G_or_1126])
        return (_G_or_1130, self.currentError)


    def rule_optResultGuard(self):
        _locals = {'self': self}
        self.locals['optResultGuard'] = _locals
        def _G_optional_1131():
            _G_python_1132, lastError = ':', None
            _G_apply_1133, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1132])
            _G_apply_1134, lastError = self._apply(self.rule_guard, "guard", [])
            return (_G_apply_1134, self.currentError)
        def _G_optional_1135():
            return (None, self.input.nullError())
        _G_or_1136, lastError = self._or([_G_optional_1131, _G_optional_1135])
        return (_G_or_1136, self.currentError)


    def rule_scriptPair(self):
        _locals = {'self': self}
        self.locals['scriptPair'] = _locals
        _G_python_1137, lastError = '{', None
        _G_apply_1138, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1137])
        def _G_many_1139():
            _G_apply_1140, lastError = self._apply(self.rule_method, "method", [])
            return (_G_apply_1140, self.currentError)
        _G_many_1141, lastError = self.many(_G_many_1139)
        _locals['methods'] = _G_many_1141
        def _G_many_1142():
            _G_apply_1143, lastError = self._apply(self.rule_matcher, "matcher", [])
            return (_G_apply_1143, self.currentError)
        _G_many_1144, lastError = self.many(_G_many_1142)
        _locals['matchers'] = _G_many_1144
        _G_python_1145, lastError = "}", None
        _G_apply_1146, lastError = self._apply(self.rule_token, "token", [_G_python_1145])
        _G_python_1147, lastError = eval('[methods, matchers]', self.globals, _locals), None
        return (_G_python_1147, self.currentError)


    def rule_method(self):
        _locals = {'self': self}
        self.locals['method'] = _locals
        def _G_optional_1148():
            _G_apply_1149, lastError = self._apply(self.rule_doco, "doco", [])
            return (_G_apply_1149, self.currentError)
        def _G_optional_1150():
            return (None, self.input.nullError())
        _G_or_1151, lastError = self._or([_G_optional_1148, _G_optional_1150])
        _locals['doc'] = _G_or_1151
        def _G_or_1152():
            _G_python_1153, lastError = "to", None
            _G_apply_1154, lastError = self._apply(self.rule_token, "token", [_G_python_1153])
            _G_python_1155, lastError = eval('t.To', self.globals, _locals), None
            return (_G_python_1155, self.currentError)
        def _G_or_1156():
            _G_python_1157, lastError = "method", None
            _G_apply_1158, lastError = self._apply(self.rule_token, "token", [_G_python_1157])
            _G_python_1159, lastError = eval('t.Method', self.globals, _locals), None
            return (_G_python_1159, self.currentError)
        _G_or_1160, lastError = self._or([_G_or_1152, _G_or_1156])
        _locals['to'] = _G_or_1160
        def _G_optional_1161():
            _G_apply_1162, lastError = self._apply(self.rule_verb, "verb", [])
            return (_G_apply_1162, self.currentError)
        def _G_optional_1163():
            return (None, self.input.nullError())
        _G_or_1164, lastError = self._or([_G_optional_1161, _G_optional_1163])
        _locals['v'] = _G_or_1164
        _G_apply_1165, lastError = self._apply(self.rule_parenParamList, "parenParamList", [])
        _locals['ps'] = _G_apply_1165
        _G_apply_1166, lastError = self._apply(self.rule_optResultGuard, "optResultGuard", [])
        _locals['g'] = _G_apply_1166
        _G_apply_1167, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1167
        _G_python_1168, lastError = eval('to(doc, v, ps, g, b)', self.globals, _locals), None
        return (_G_python_1168, self.currentError)


    def rule_matcher(self):
        _locals = {'self': self}
        self.locals['matcher'] = _locals
        _G_python_1169, lastError = "match", None
        _G_apply_1170, lastError = self._apply(self.rule_token, "token", [_G_python_1169])
        _G_apply_1171, lastError = self._apply(self.rule_pattern, "pattern", [])
        _locals['p'] = _G_apply_1171
        _G_apply_1172, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1172
        _G_python_1173, lastError = eval('t.Matcher(p, b)', self.globals, _locals), None
        return (_G_python_1173, self.currentError)


    def rule_interfaceExpr(self):
        _locals = {'self': self}
        self.locals['interfaceExpr'] = _locals
        _G_python_1174, lastError = "interface", None
        _G_apply_1175, lastError = self._apply(self.rule_token, "token", [_G_python_1174])
        _G_apply_1176, lastError = self._apply(self.rule_objectName, "objectName", [])
        _locals['n'] = _G_apply_1176
        def _G_optional_1177():
            _G_apply_1178, lastError = self._apply(self.rule_iguards, "iguards", [])
            return (_G_apply_1178, self.currentError)
        def _G_optional_1179():
            return (None, self.input.nullError())
        _G_or_1180, lastError = self._or([_G_optional_1177, _G_optional_1179])
        _locals['g'] = _G_or_1180
        def _G_or_1181():
            _G_apply_1182, lastError = self._apply(self.rule_multiExtends, "multiExtends", [])
            _locals['es'] = _G_apply_1182
            _G_apply_1183, lastError = self._apply(self.rule_oImplements, "oImplements", [])
            _locals['oi'] = _G_apply_1183
            _G_apply_1184, lastError = self._apply(self.rule_iscript, "iscript", [])
            _locals['s'] = _G_apply_1184
            _G_python_1185, lastError = eval('[n, g, es, oi, s]', self.globals, _locals), None
            return (_G_python_1185, self.currentError)
        def _G_or_1186():
            _G_apply_1187, lastError = self._apply(self.rule_parenParamDescList, "parenParamDescList", [])
            _locals['ps'] = _G_apply_1187
            _G_apply_1188, lastError = self._apply(self.rule_optGuard, "optGuard", [])
            _locals['rg'] = _G_apply_1188
            _G_python_1189, lastError = eval('[n, g, [], [], t.InterfaceFunction(ps, rg)]', self.globals, _locals), None
            return (_G_python_1189, self.currentError)
        _G_or_1190, lastError = self._or([_G_or_1181, _G_or_1186])
        return (_G_or_1190, self.currentError)


    def rule_iguards(self):
        _locals = {'self': self}
        self.locals['iguards'] = _locals
        _G_python_1191, lastError = "guards", None
        _G_apply_1192, lastError = self._apply(self.rule_token, "token", [_G_python_1191])
        _G_apply_1193, lastError = self._apply(self.rule_pattern, "pattern", [])
        return (_G_apply_1193, self.currentError)


    def rule_multiExtends(self):
        _locals = {'self': self}
        self.locals['multiExtends'] = _locals
        def _G_or_1194():
            _G_python_1195, lastError = "extends", None
            _G_apply_1196, lastError = self._apply(self.rule_token, "token", [_G_python_1195])
            _G_apply_1197, lastError = self._apply(self.rule_br, "br", [])
            _G_apply_1198, lastError = self._apply(self.rule_order, "order", [])
            _locals['x'] = _G_apply_1198
            def _G_many_1199():
                _G_python_1200, lastError = ',', None
                _G_apply_1201, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1200])
                _G_apply_1202, lastError = self._apply(self.rule_order, "order", [])
                return (_G_apply_1202, self.currentError)
            _G_many_1203, lastError = self.many(_G_many_1199)
            _locals['xs'] = _G_many_1203
            _G_python_1204, lastError = eval('[x] + xs', self.globals, _locals), None
            return (_G_python_1204, self.currentError)
        def _G_or_1205():
            _G_python_1206, lastError = [], None
            return (_G_python_1206, self.currentError)
        _G_or_1207, lastError = self._or([_G_or_1194, _G_or_1205])
        return (_G_or_1207, self.currentError)


    def rule_iscript(self):
        _locals = {'self': self}
        self.locals['iscript'] = _locals
        _G_python_1208, lastError = '{', None
        _G_apply_1209, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1208])
        def _G_many_1210():
            _G_apply_1211, lastError = self._apply(self.rule_messageDesc, "messageDesc", [])
            _locals['m'] = _G_apply_1211
            _G_apply_1212, lastError = self._apply(self.rule_br, "br", [])
            _G_python_1213, lastError = eval('m', self.globals, _locals), None
            return (_G_python_1213, self.currentError)
        _G_many_1214, lastError = self.many(_G_many_1210)
        _locals['ms'] = _G_many_1214
        _G_python_1215, lastError = "}", None
        _G_apply_1216, lastError = self._apply(self.rule_token, "token", [_G_python_1215])
        _G_python_1217, lastError = eval('ms', self.globals, _locals), None
        return (_G_python_1217, self.currentError)


    def rule_messageDesc(self):
        _locals = {'self': self}
        self.locals['messageDesc'] = _locals
        def _G_optional_1218():
            _G_apply_1219, lastError = self._apply(self.rule_doco, "doco", [])
            return (_G_apply_1219, self.currentError)
        def _G_optional_1220():
            return (None, self.input.nullError())
        _G_or_1221, lastError = self._or([_G_optional_1218, _G_optional_1220])
        _locals['doc'] = _G_or_1221
        def _G_or_1222():
            _G_python_1223, lastError = "to", None
            _G_apply_1224, lastError = self._apply(self.rule_token, "token", [_G_python_1223])
            return (_G_apply_1224, self.currentError)
        def _G_or_1225():
            _G_python_1226, lastError = "method", None
            _G_apply_1227, lastError = self._apply(self.rule_token, "token", [_G_python_1226])
            return (_G_apply_1227, self.currentError)
        _G_or_1228, lastError = self._or([_G_or_1222, _G_or_1225])
        _locals['to'] = _G_or_1228
        def _G_optional_1229():
            _G_apply_1230, lastError = self._apply(self.rule_verb, "verb", [])
            return (_G_apply_1230, self.currentError)
        def _G_optional_1231():
            return (None, self.input.nullError())
        _G_or_1232, lastError = self._or([_G_optional_1229, _G_optional_1231])
        _locals['v'] = _G_or_1232
        _G_apply_1233, lastError = self._apply(self.rule_parenParamDescList, "parenParamDescList", [])
        _locals['ps'] = _G_apply_1233
        _G_apply_1234, lastError = self._apply(self.rule_optGuard, "optGuard", [])
        _locals['g'] = _G_apply_1234
        _G_python_1235, lastError = eval('t.MessageDesc(doc, to, v, ps, g)', self.globals, _locals), None
        return (_G_python_1235, self.currentError)


    def rule_paramDesc(self):
        _locals = {'self': self}
        self.locals['paramDesc'] = _locals
        def _G_or_1236():
            _G_apply_1237, lastError = self._apply(self.rule_justNoun, "justNoun", [])
            return (_G_apply_1237, self.currentError)
        def _G_or_1238():
            _G_python_1239, lastError = '_', None
            _G_apply_1240, lastError = self._apply(self.rule_token, "token", [_G_python_1239])
            _G_python_1241, lastError = None, None
            return (_G_python_1241, self.currentError)
        _G_or_1242, lastError = self._or([_G_or_1236, _G_or_1238])
        _locals['n'] = _G_or_1242
        _G_apply_1243, lastError = self._apply(self.rule_optGuard, "optGuard", [])
        _locals['g'] = _G_apply_1243
        _G_python_1244, lastError = eval('t.ParamDesc(n, g)', self.globals, _locals), None
        return (_G_python_1244, self.currentError)


    def rule_parenParamDescList(self):
        _locals = {'self': self}
        self.locals['parenParamDescList'] = _locals
        _G_python_1245, lastError = '(', None
        _G_apply_1246, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1245])
        _G_apply_1247, lastError = self._apply(self.rule_paramDesc, "paramDesc", [])
        _locals['p'] = _G_apply_1247
        def _G_many_1248():
            _G_python_1249, lastError = ',', None
            _G_apply_1250, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1249])
            _G_apply_1251, lastError = self._apply(self.rule_paramDesc, "paramDesc", [])
            return (_G_apply_1251, self.currentError)
        _G_many_1252, lastError = self.many(_G_many_1248)
        _locals['ps'] = _G_many_1252
        _G_python_1253, lastError = ")", None
        _G_apply_1254, lastError = self._apply(self.rule_token, "token", [_G_python_1253])
        _G_python_1255, lastError = eval('[p] +  ps', self.globals, _locals), None
        return (_G_python_1255, self.currentError)


    def rule_accumExpr(self):
        _locals = {'self': self}
        self.locals['accumExpr'] = _locals
        _G_python_1256, lastError = "accum", None
        _G_apply_1257, lastError = self._apply(self.rule_token, "token", [_G_python_1256])
        _G_apply_1258, lastError = self._apply(self.rule_call, "call", [])
        _locals['c'] = _G_apply_1258
        _G_apply_1259, lastError = self._apply(self.rule_accumulator, "accumulator", [])
        _locals['a'] = _G_apply_1259
        _G_python_1260, lastError = eval('t.Accum(c, a)', self.globals, _locals), None
        return (_G_python_1260, self.currentError)


    def rule_accumulator(self):
        _locals = {'self': self}
        self.locals['accumulator'] = _locals
        def _G_or_1261():
            _G_python_1262, lastError = "for", None
            _G_apply_1263, lastError = self._apply(self.rule_token, "token", [_G_python_1262])
            _G_apply_1264, lastError = self._apply(self.rule_forPattern, "forPattern", [])
            _locals['p'] = _G_apply_1264
            _G_python_1265, lastError = "in", None
            _G_apply_1266, lastError = self._apply(self.rule_token, "token", [_G_python_1265])
            _G_apply_1267, lastError = self._apply(self.rule_logical, "logical", [])
            _locals['a'] = _G_apply_1267
            _G_apply_1268, lastError = self._apply(self.rule_accumBody, "accumBody", [])
            _locals['b'] = _G_apply_1268
            def _G_optional_1269():
                _G_apply_1270, lastError = self._apply(self.rule_catcher, "catcher", [])
                return (_G_apply_1270, self.currentError)
            def _G_optional_1271():
                return (None, self.input.nullError())
            _G_or_1272, lastError = self._or([_G_optional_1269, _G_optional_1271])
            _locals['c'] = _G_or_1272
            _G_python_1273, lastError = eval('t.AccumFor(*(p + [a, b, c]))', self.globals, _locals), None
            return (_G_python_1273, self.currentError)
        def _G_or_1274():
            _G_python_1275, lastError = "if", None
            _G_apply_1276, lastError = self._apply(self.rule_token, "token", [_G_python_1275])
            _G_apply_1277, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
            _locals['e'] = _G_apply_1277
            _G_apply_1278, lastError = self._apply(self.rule_accumBody, "accumBody", [])
            _locals['a'] = _G_apply_1278
            _G_python_1279, lastError = eval('t.AccumIf(e, a)', self.globals, _locals), None
            return (_G_python_1279, self.currentError)
        def _G_or_1280():
            _G_python_1281, lastError = "while", None
            _G_apply_1282, lastError = self._apply(self.rule_token, "token", [_G_python_1281])
            _G_apply_1283, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
            _locals['e'] = _G_apply_1283
            _G_apply_1284, lastError = self._apply(self.rule_accumBody, "accumBody", [])
            _locals['a'] = _G_apply_1284
            def _G_optional_1285():
                _G_apply_1286, lastError = self._apply(self.rule_catcher, "catcher", [])
                return (_G_apply_1286, self.currentError)
            def _G_optional_1287():
                return (None, self.input.nullError())
            _G_or_1288, lastError = self._or([_G_optional_1285, _G_optional_1287])
            _locals['c'] = _G_or_1288
            _G_python_1289, lastError = eval('t.AccumWhile(e, a, c)', self.globals, _locals), None
            return (_G_python_1289, self.currentError)
        _G_or_1290, lastError = self._or([_G_or_1261, _G_or_1274, _G_or_1280])
        return (_G_or_1290, self.currentError)


    def rule_accumBody(self):
        _locals = {'self': self}
        self.locals['accumBody'] = _locals
        _G_python_1291, lastError = '{', None
        _G_apply_1292, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1291])
        def _G_or_1293():
            _G_python_1294, lastError = '_', None
            _G_apply_1295, lastError = self._apply(self.rule_token, "token", [_G_python_1294])
            def _G_or_1296():
                _G_apply_1297, lastError = self._apply(self.rule_accumOp, "accumOp", [])
                _locals['op'] = _G_apply_1297
                _G_apply_1298, lastError = self._apply(self.rule_assign, "assign", [])
                _locals['a'] = _G_apply_1298
                _G_python_1299, lastError = eval('t.AccumOp(op, a)', self.globals, _locals), None
                return (_G_python_1299, self.currentError)
            def _G_or_1300():
                _G_python_1301, lastError = '.', None
                _G_apply_1302, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1301])
                _G_apply_1303, lastError = self._apply(self.rule_verb, "verb", [])
                _locals['v'] = _G_apply_1303
                _G_apply_1304, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
                _locals['ps'] = _G_apply_1304
                _G_python_1305, lastError = eval('t.AccumCall(v, ps)', self.globals, _locals), None
                return (_G_python_1305, self.currentError)
            _G_or_1306, lastError = self._or([_G_or_1296, _G_or_1300])
            return (_G_or_1306, self.currentError)
        def _G_or_1307():
            _G_apply_1308, lastError = self._apply(self.rule_accumulator, "accumulator", [])
            return (_G_apply_1308, self.currentError)
        _G_or_1309, lastError = self._or([_G_or_1293, _G_or_1307])
        _locals['ab'] = _G_or_1309
        _G_apply_1310, lastError = self._apply(self.rule_br, "br", [])
        _G_python_1311, lastError = "}", None
        _G_apply_1312, lastError = self._apply(self.rule_token, "token", [_G_python_1311])
        _G_python_1313, lastError = eval('ab', self.globals, _locals), None
        return (_G_python_1313, self.currentError)


    def rule_accumOp(self):
        _locals = {'self': self}
        self.locals['accumOp'] = _locals
        def _G_or_1314():
            _G_python_1315, lastError = '+', None
            _G_apply_1316, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1315])
            _G_python_1317, lastError = "Add", None
            return (_G_python_1317, self.currentError)
        def _G_or_1318():
            _G_python_1319, lastError = '*', None
            _G_apply_1320, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1319])
            _G_python_1321, lastError = "Multiply", None
            return (_G_python_1321, self.currentError)
        def _G_or_1322():
            _G_python_1323, lastError = '&', None
            _G_apply_1324, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1323])
            _G_python_1325, lastError = "BinaryAnd", None
            return (_G_python_1325, self.currentError)
        def _G_or_1326():
            _G_python_1327, lastError = '|', None
            _G_apply_1328, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1327])
            _G_python_1329, lastError = "BinaryOr", None
            return (_G_python_1329, self.currentError)
        _G_or_1330, lastError = self._or([_G_or_1314, _G_or_1318, _G_or_1322, _G_or_1326])
        return (_G_or_1330, self.currentError)


    def rule_escapeExpr(self):
        _locals = {'self': self}
        self.locals['escapeExpr'] = _locals
        _G_python_1331, lastError = "escape", None
        _G_apply_1332, lastError = self._apply(self.rule_token, "token", [_G_python_1331])
        _G_apply_1333, lastError = self._apply(self.rule_pattern, "pattern", [])
        _locals['p'] = _G_apply_1333
        _G_apply_1334, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1334
        def _G_optional_1335():
            _G_apply_1336, lastError = self._apply(self.rule_catcher, "catcher", [])
            return (_G_apply_1336, self.currentError)
        def _G_optional_1337():
            return (None, self.input.nullError())
        _G_or_1338, lastError = self._or([_G_optional_1335, _G_optional_1337])
        _locals['c'] = _G_or_1338
        _G_python_1339, lastError = eval('t.Escape(p, b, c)', self.globals, _locals), None
        return (_G_python_1339, self.currentError)


    def rule_forExpr(self):
        _locals = {'self': self}
        self.locals['forExpr'] = _locals
        _G_python_1340, lastError = "for", None
        _G_apply_1341, lastError = self._apply(self.rule_token, "token", [_G_python_1340])
        _G_apply_1342, lastError = self._apply(self.rule_forPattern, "forPattern", [])
        _locals['p'] = _G_apply_1342
        _G_python_1343, lastError = "in", None
        _G_apply_1344, lastError = self._apply(self.rule_token, "token", [_G_python_1343])
        _G_apply_1345, lastError = self._apply(self.rule_br, "br", [])
        _G_apply_1346, lastError = self._apply(self.rule_assign, "assign", [])
        _locals['a'] = _G_apply_1346
        _G_apply_1347, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1347
        def _G_optional_1348():
            _G_apply_1349, lastError = self._apply(self.rule_catcher, "catcher", [])
            return (_G_apply_1349, self.currentError)
        def _G_optional_1350():
            return (None, self.input.nullError())
        _G_or_1351, lastError = self._or([_G_optional_1348, _G_optional_1350])
        _locals['c'] = _G_or_1351
        _G_python_1352, lastError = eval('t.For(*(p + [a, b, c]))', self.globals, _locals), None
        return (_G_python_1352, self.currentError)


    def rule_forPattern(self):
        _locals = {'self': self}
        self.locals['forPattern'] = _locals
        _G_apply_1353, lastError = self._apply(self.rule_pattern, "pattern", [])
        _locals['p'] = _G_apply_1353
        def _G_or_1354():
            _G_apply_1355, lastError = self._apply(self.rule_br, "br", [])
            _G_python_1356, lastError = '=>', None
            _G_apply_1357, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1356])
            _G_apply_1358, lastError = self._apply(self.rule_pattern, "pattern", [])
            _locals['px'] = _G_apply_1358
            _G_python_1359, lastError = eval('[p, px]', self.globals, _locals), None
            return (_G_python_1359, self.currentError)
        def _G_or_1360():
            _G_python_1361, lastError = eval('[None, p]', self.globals, _locals), None
            return (_G_python_1361, self.currentError)
        _G_or_1362, lastError = self._or([_G_or_1354, _G_or_1360])
        return (_G_or_1362, self.currentError)


    def rule_ifExpr(self):
        _locals = {'self': self}
        self.locals['ifExpr'] = _locals
        _G_python_1363, lastError = "if", None
        _G_apply_1364, lastError = self._apply(self.rule_token, "token", [_G_python_1363])
        _G_apply_1365, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
        _locals['p'] = _G_apply_1365
        _G_apply_1366, lastError = self._apply(self.rule_br, "br", [])
        _G_apply_1367, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1367
        def _G_or_1368():
            _G_python_1369, lastError = "else", None
            _G_apply_1370, lastError = self._apply(self.rule_token, "token", [_G_python_1369])
            def _G_or_1371():
                _G_apply_1372, lastError = self._apply(self.rule_ifExpr, "ifExpr", [])
                return (_G_apply_1372, self.currentError)
            def _G_or_1373():
                _G_apply_1374, lastError = self._apply(self.rule_block, "block", [])
                return (_G_apply_1374, self.currentError)
            _G_or_1375, lastError = self._or([_G_or_1371, _G_or_1373])
            return (_G_or_1375, self.currentError)
        def _G_or_1376():
            _G_python_1377, lastError = None, None
            return (_G_python_1377, self.currentError)
        _G_or_1378, lastError = self._or([_G_or_1368, _G_or_1376])
        _locals['e'] = _G_or_1378
        _G_python_1379, lastError = eval('t.If(p, b, e)', self.globals, _locals), None
        return (_G_python_1379, self.currentError)


    def rule_lambdaExpr(self):
        _locals = {'self': self}
        self.locals['lambdaExpr'] = _locals
        def _G_optional_1380():
            _G_apply_1381, lastError = self._apply(self.rule_doco, "doco", [])
            return (_G_apply_1381, self.currentError)
        def _G_optional_1382():
            return (None, self.input.nullError())
        _G_or_1383, lastError = self._or([_G_optional_1380, _G_optional_1382])
        _locals['doc'] = _G_or_1383
        _G_python_1384, lastError = "fn", None
        _G_apply_1385, lastError = self._apply(self.rule_token, "token", [_G_python_1384])
        _G_apply_1386, lastError = self._apply(self.rule_patterns, "patterns", [])
        _locals['ps'] = _G_apply_1386
        _G_apply_1387, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1387
        _G_python_1388, lastError = eval('t.Lambda(doc, ps, b)', self.globals, _locals), None
        return (_G_python_1388, self.currentError)


    def rule_metaExpr(self):
        _locals = {'self': self}
        self.locals['metaExpr'] = _locals
        _G_python_1389, lastError = "meta", None
        _G_apply_1390, lastError = self._apply(self.rule_token, "token", [_G_python_1389])
        _G_python_1391, lastError = '.', None
        _G_apply_1392, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1391])
        def _G_or_1393():
            _G_python_1394, lastError = "getState", None
            _G_apply_1395, lastError = self._apply(self.rule_token, "token", [_G_python_1394])
            _G_python_1396, lastError = "State", None
            return (_G_python_1396, self.currentError)
        def _G_or_1397():
            _G_python_1398, lastError = "scope", None
            _G_apply_1399, lastError = self._apply(self.rule_token, "token", [_G_python_1398])
            _G_python_1400, lastError = "Scope", None
            return (_G_python_1400, self.currentError)
        def _G_or_1401():
            _G_python_1402, lastError = "context", None
            _G_apply_1403, lastError = self._apply(self.rule_token, "token", [_G_python_1402])
            _G_python_1404, lastError = "Context", None
            return (_G_python_1404, self.currentError)
        _G_or_1405, lastError = self._or([_G_or_1393, _G_or_1397, _G_or_1401])
        _locals['s'] = _G_or_1405
        _G_python_1406, lastError = '(', None
        _G_apply_1407, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1406])
        _G_python_1408, lastError = ")", None
        _G_apply_1409, lastError = self._apply(self.rule_token, "token", [_G_python_1408])
        _G_python_1410, lastError = eval('t.Meta(s)', self.globals, _locals), None
        return (_G_python_1410, self.currentError)


    def rule_switchExpr(self):
        _locals = {'self': self}
        self.locals['switchExpr'] = _locals
        _G_python_1411, lastError = "switch", None
        _G_apply_1412, lastError = self._apply(self.rule_token, "token", [_G_python_1411])
        _G_apply_1413, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
        _locals['e'] = _G_apply_1413
        _G_python_1414, lastError = '{', None
        _G_apply_1415, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1414])
        def _G_many_1416():
            _G_apply_1417, lastError = self._apply(self.rule_matcher, "matcher", [])
            _locals['m'] = _G_apply_1417
            _G_apply_1418, lastError = self._apply(self.rule_br, "br", [])
            _G_python_1419, lastError = eval('m', self.globals, _locals), None
            return (_G_python_1419, self.currentError)
        _G_many_1420, lastError = self.many(_G_many_1416)
        _locals['ms'] = _G_many_1420
        _G_python_1421, lastError = "}", None
        _G_apply_1422, lastError = self._apply(self.rule_token, "token", [_G_python_1421])
        _G_python_1423, lastError = eval('t.Switch(e, ms)', self.globals, _locals), None
        return (_G_python_1423, self.currentError)


    def rule_tryExpr(self):
        _locals = {'self': self}
        self.locals['tryExpr'] = _locals
        _G_python_1424, lastError = "try", None
        _G_apply_1425, lastError = self._apply(self.rule_token, "token", [_G_python_1424])
        _G_apply_1426, lastError = self._apply(self.rule_block, "block", [])
        _locals['tb'] = _G_apply_1426
        def _G_many_1427():
            _G_apply_1428, lastError = self._apply(self.rule_catcher, "catcher", [])
            return (_G_apply_1428, self.currentError)
        _G_many_1429, lastError = self.many(_G_many_1427)
        _locals['cs'] = _G_many_1429
        def _G_optional_1430():
            _G_python_1431, lastError = "finally", None
            _G_apply_1432, lastError = self._apply(self.rule_token, "token", [_G_python_1431])
            _G_apply_1433, lastError = self._apply(self.rule_block, "block", [])
            return (_G_apply_1433, self.currentError)
        def _G_optional_1434():
            return (None, self.input.nullError())
        _G_or_1435, lastError = self._or([_G_optional_1430, _G_optional_1434])
        _locals['fb'] = _G_or_1435
        _G_python_1436, lastError = eval('t.Try(tb, cs, fb)', self.globals, _locals), None
        return (_G_python_1436, self.currentError)


    def rule_catcher(self):
        _locals = {'self': self}
        self.locals['catcher'] = _locals
        _G_python_1437, lastError = "catch", None
        _G_apply_1438, lastError = self._apply(self.rule_token, "token", [_G_python_1437])
        _G_apply_1439, lastError = self._apply(self.rule_pattern, "pattern", [])
        _locals['p'] = _G_apply_1439
        _G_apply_1440, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1440
        _G_python_1441, lastError = eval('t.Catch(p, b)', self.globals, _locals), None
        return (_G_python_1441, self.currentError)


    def rule_whileExpr(self):
        _locals = {'self': self}
        self.locals['whileExpr'] = _locals
        _G_python_1442, lastError = "while", None
        _G_apply_1443, lastError = self._apply(self.rule_token, "token", [_G_python_1442])
        _G_apply_1444, lastError = self._apply(self.rule_parenExpr, "parenExpr", [])
        _locals['e'] = _G_apply_1444
        _G_apply_1445, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1445
        def _G_optional_1446():
            _G_apply_1447, lastError = self._apply(self.rule_catcher, "catcher", [])
            return (_G_apply_1447, self.currentError)
        def _G_optional_1448():
            return (None, self.input.nullError())
        _G_or_1449, lastError = self._or([_G_optional_1446, _G_optional_1448])
        _locals['c'] = _G_or_1449
        _G_python_1450, lastError = eval('t.While(e, b, c)', self.globals, _locals), None
        return (_G_python_1450, self.currentError)


    def rule_whenExpr(self):
        _locals = {'self': self}
        self.locals['whenExpr'] = _locals
        _G_python_1451, lastError = "when", None
        _G_apply_1452, lastError = self._apply(self.rule_token, "token", [_G_python_1451])
        _G_apply_1453, lastError = self._apply(self.rule_parenArgs, "parenArgs", [])
        _locals['a'] = _G_apply_1453
        _G_apply_1454, lastError = self._apply(self.rule_br, "br", [])
        _G_python_1455, lastError = '->', None
        _G_apply_1456, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1455])
        _G_apply_1457, lastError = self._apply(self.rule_block, "block", [])
        _locals['b'] = _G_apply_1457
        def _G_many_1458():
            _G_apply_1459, lastError = self._apply(self.rule_catcher, "catcher", [])
            return (_G_apply_1459, self.currentError)
        _G_many_1460, lastError = self.many(_G_many_1458)
        _locals['cs'] = _G_many_1460
        def _G_optional_1461():
            _G_python_1462, lastError = "finally", None
            _G_apply_1463, lastError = self._apply(self.rule_token, "token", [_G_python_1462])
            _G_apply_1464, lastError = self._apply(self.rule_block, "block", [])
            return (_G_apply_1464, self.currentError)
        def _G_optional_1465():
            return (None, self.input.nullError())
        _G_or_1466, lastError = self._or([_G_optional_1461, _G_optional_1465])
        _locals['fb'] = _G_or_1466
        _G_python_1467, lastError = eval('t.When(a, b, cs, fb)', self.globals, _locals), None
        return (_G_python_1467, self.currentError)


    def rule_topSeq(self):
        _locals = {'self': self}
        self.locals['topSeq'] = _locals
        _G_apply_1468, lastError = self._apply(self.rule_topExpr, "topExpr", [])
        _locals['x'] = _G_apply_1468
        def _G_many_1469():
            _G_apply_1470, lastError = self._apply(self.rule_seqSep, "seqSep", [])
            _G_apply_1471, lastError = self._apply(self.rule_topExpr, "topExpr", [])
            return (_G_apply_1471, self.currentError)
        _G_many_1472, lastError = self.many(_G_many_1469)
        _locals['xs'] = _G_many_1472
        def _G_optional_1473():
            _G_apply_1474, lastError = self._apply(self.rule_seqSep, "seqSep", [])
            return (_G_apply_1474, self.currentError)
        def _G_optional_1475():
            return (None, self.input.nullError())
        _G_or_1476, lastError = self._or([_G_optional_1473, _G_optional_1475])
        _G_python_1477, lastError = eval('t.SeqExpr([x] + xs)', self.globals, _locals), None
        return (_G_python_1477, self.currentError)


    def rule_pragma(self):
        _locals = {'self': self}
        self.locals['pragma'] = _locals
        _G_python_1478, lastError = "pragma", None
        _G_apply_1479, lastError = self._apply(self.rule_token, "token", [_G_python_1478])
        _G_python_1480, lastError = '.', None
        _G_apply_1481, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1480])
        _G_apply_1482, lastError = self._apply(self.rule_verb, "verb", [])
        _locals['v'] = _G_apply_1482
        _G_python_1483, lastError = '(', None
        _G_apply_1484, lastError = self._apply(self.rule_tokenBR, "tokenBR", [_G_python_1483])
        _G_apply_1485, lastError = self._apply(self.rule_string, "string", [])
        _locals['s'] = _G_apply_1485
        _G_python_1486, lastError = ")", None
        _G_apply_1487, lastError = self._apply(self.rule_token, "token", [_G_python_1486])
        _G_python_1488, lastError = eval('t.Pragma(v, s)', self.globals, _locals), None
        return (_G_python_1488, self.currentError)


    def rule_topExpr(self):
        _locals = {'self': self}
        self.locals['topExpr'] = _locals
        def _G_or_1489():
            _G_apply_1490, lastError = self._apply(self.rule_pragma, "pragma", [])
            _G_python_1491, lastError = eval('t.NounExpr("null")', self.globals, _locals), None
            return (_G_python_1491, self.currentError)
        def _G_or_1492():
            _G_apply_1493, lastError = self._apply(self.rule_expr, "expr", [])
            return (_G_apply_1493, self.currentError)
        _G_or_1494, lastError = self._or([_G_or_1489, _G_or_1492])
        return (_G_or_1494, self.currentError)


    def rule_start(self):
        _locals = {'self': self}
        self.locals['start'] = _locals
        def _G_optional_1495():
            _G_apply_1496, lastError = self._apply(self.rule_updoc, "updoc", [])
            return (_G_apply_1496, self.currentError)
        def _G_optional_1497():
            return (None, self.input.nullError())
        _G_or_1498, lastError = self._or([_G_optional_1495, _G_optional_1497])
        _G_apply_1499, lastError = self._apply(self.rule_br, "br", [])
        def _G_optional_1500():
            _G_apply_1501, lastError = self._apply(self.rule_topSeq, "topSeq", [])
            return (_G_apply_1501, self.currentError)
        def _G_optional_1502():
            return (None, self.input.nullError())
        _G_or_1503, lastError = self._or([_G_optional_1500, _G_optional_1502])
        return (_G_or_1503, self.currentError)
