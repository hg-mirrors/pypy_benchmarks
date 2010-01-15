USSVN="http://unladen-swallow.googlecode.com/svn"

find unladen-swallow -iname ".svn" -prune -a -iname ".svn" -false -o -type f|rm -rf

svn export --force --depth files $USSVN/tests unladen-swallow

svn export --force $USSVN/tests/performance unladen-swallow/performance

DIRECT_LIBS="google_appengine lockfile html5lib"

for lib in $DIRECT_LIBS; do
    svn export --force $USSVN/tests/lib/$lib unladen-swallow/lib/$lib
done

EXTERNAL_LIBS="spitfire|django|rietveld|spambayes"

svn pget svn:externals http://unladen-swallow.googlecode.com/svn/tests|grep -E $EXTERNAL_LIBS|sed -e s[lib/[unladen-swallow/lib/[ |xargs -I{} -n1 sh -c "svn export --force {}"