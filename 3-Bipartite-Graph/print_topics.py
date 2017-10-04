import gensim
import os
if os.path.exists('models/new-model.lda'):
    ldamodel = gensim.models.ldamodel.LdaModel.load('models/new-model.lda')
    for i in range(0, ldamodel.num_topics):
        print "Topic #" + str(i) + ":",
        print ldamodel.print_topic(i)
        print ""
