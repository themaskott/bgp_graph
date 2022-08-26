# bgp_graph


For the moment I'm just trying stuff to play with the graph of the ASes.


First dump a bveiw to a text file :

`bgpdump -M -O dump.txt bview.gz`

Then, just AS pathes are needed, so extract them :

`cut -d "|" dump.txt -f7 | sort | uniq > uniq_path.txt`
