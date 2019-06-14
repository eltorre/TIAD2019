=== `reel.py`

The python version of reel is better suited for pulling small graphs. Performance degrades rather quick.

Requires Elementtree and igraph (`python-igraph`, beware there is a pip package that goes for the name `igraph`; also you need imagemagick/convert to install this package). Pretty much alpha and prone to breaking. Check the parameters by running `./reel -h`

For example:

`~./reel.py -w banco -l es -f es pt apertium-es-pt.es-pt.dix -f en es apertium-eng-spa.eng-spa.dix -f fr es apertium-fr-es.fr-es.dix -d 5 -m -g`

Will return both a list of links via stdout and a graph (in a temporary file opened using imagemagick). 
Each word is in the form `surface|POS|language`, where language is the name given as parameter (e.g. es for Spanish in this example). The different POS classes are defined in the "header" of the bilingual dictionary file (`<sdefs>`).

The `d3js` mode can be used to generate a d3-like json file. Dump the output into `web/data.json`, serve the folder (e.g. `python -m SimpleHTTPServer`) and open `index.html` to see the representation.

==== `reel.cc`

The c file was used to generate the dictionaries for the submission. DFS is used to generate all length-4 cycles. Check `example` for an imput example. 

Code for the DFS was copied from https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

==== Apertium bilingual dictionary format simplified reference

Apertium refers to the languages as `R` for the "right" language and `L` for the "left" language; e.g. eng-spa L=eng R=spa

* `dictionary`
 * `alphabet` > defines the alphabet, not usually ysed
 * `sdefs` > the POS classes
  * `sdef` > each POS class
 * `section` > a section of the dictionary. `@id=main` is always there. Additionally, you might find other sections with automatically generated entries or regular expressions
  * `e` > an entry
   * `@r="RL"` > means that the entry is only valid when translating from right to left language. There is also LR. Default is both directions are fine
   * `p` > a pair
     * `l` > the left word
     * `r` > the right word
    * `i` > an identity. It is exclusive with `p`, and, while it is discouraged, still shows in old dicts.

Each `p` or `i` have
* Plain text with the word in canonical form, mixed with `<g>` and `<b/>` in the case of multiwords, e.g. `<r>seguro<g><b/>de<b/>vida</g><s n="n"/>`, _seguro_ is a word that can be flexed and _de vida_ is the invariable part
* `s` POS info
 * `@n` the POS