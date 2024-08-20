#!/bin/bash
set +x
#
# text  nlptoolsCLI.py en mode CLI
# mode developpement
# usage :
#     ./test/cli/test_nlptoolsCLI.sh
# resultat dans "result.txt"
#
NLP_TOOLS=$HOME/app/NLP_tools
CLI=$NLP_TOOLS/test/cli
DATA=$NLP_TOOLS/test/data
INI_EN=$NLP_TOOLS/test/conf_test_en.ini
INI_FR=$NLP_TOOLS/test/conf_test_fr.ini

engine_en="stemmer POStagger ner NPchunker NPchunkerDP termMatcher" #termMatcher
engine_fr="stemmer lefff_tagger"

file_result=result_test_nlptoolsCLI.txt
out_format="json doc list"
cat /dev/null >| $CLI/$file_result

test_()
{
  if eval $cmd >> $CLI/$file_result; then
    echo "commande OK : $cmd"
  else
    echo "commande ERROR : $NLP_TOOLS/$cmd"
  fi
}

for elt in $engine_en
do
  echo "" >> $CLI/$file_result
  echo "****** Test engine = $elt en ******************************************" >> $CLI/$file_result
   echo "" >> $CLI/$file_result
  echo "elt =" $elt  $CLI/$file_result  >> $CLI/$file_result

  for out in $out_format
  do
      echo "--------------------------------------- Input TXT -  show= $out" >> $CLI/$file_result
      cmd="cat $DATA/not-en.txt | python3 $NLP_TOOLS/nlptools/nlptoolsCLI.py $elt -ini_file $INI_EN -lang en -f txt -o $out -log  analyze.log"
      test_
      echo "--------------------------------------- Input TSV - show= $out" >> $CLI/$file_result
      # input tsv - output list
      cmd="cat $DATA/not-en.tsv | python3 $NLP_TOOLS/nlptools/nlptoolsCLI.py $elt -ini_file $INI_EN -lang en -f txt -o $out -log  analyze.log"
      test_
  done

done

for elt in $engine_fr
do
  echo "" >> $CLI/$file_result
  echo "****** Test engine = $elt fr---------------------------"  >> $CLI/$file_result
  echo "elt =" $elt  >> $CLI/$file_result

  for out in $out_format
  do
     echo "--------------------------------------- Input TXT - show= $out" >> $CLI/$file_result
    cmd="cat $DATA/not-fr.txt | python3  $NLP_TOOLS/nlptools/nlptoolsCLI.py $elt  -ini_file $INI_FR -lang fr -f txt -o $out -log  analyze.log"
    test_
  done

done