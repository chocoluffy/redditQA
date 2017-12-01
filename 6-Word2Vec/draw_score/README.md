 `numactl --interleave=all ./mongodb/mongodb-linux-x86_64-3.4.10/bin/mongod --dbpath ./data/db/`

In [3]: lda_overlap
Out[3]: LinregressResult(slope=0.23396059546618864, intercept=53.192709922136984, rvalue=0.22798805556086676, pvalue=0.0, stderr=0.0029954251149099213)

In [4]: lda_entropy
Out[4]: LinregressResult(slope=0.063738345766101712, intercept=57.515730139118631, rvalue=0.048338168566090703, pvalue=1.4874406947225274e-58, stderr=0.0039484021792477687)

In [5]: overlap_entropy
Out[5]: LinregressResult(slope=-0.031384983827901121, intercept=63.89507608449518, rvalue=-0.024425414174207981, pvalue=3.679337094064735e-16, stderr=0.0038509612262872788)