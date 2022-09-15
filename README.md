# bgp_graph

Some scripts to compute graphes of ASes from BGP announcements.

- Full ASes graph
- Only french ASes graph
- French ASes graph with foreign neighbours

Include some metrics and features to play with those graphes.

### Pre requisite

First dump a bview to a text file :

`bgpdump -M -O dump.txt bview.gz`

Then, just AS pathes are needed, so extract them :

`cut -d "|" dump.txt -f7 | sort | uniq > uniq_path.txt`


Some input files are needed :

`datas/dump.txt` and `datas/uniq_path.txt` : see below

`datas/AS.json` and `datas/AS_FR.json` : dictionary of all AS and french ASes (see `autnums.py`)


### Usage

```bash
$ python3 bgp_graph.py -h
usage: bgp_graph.py [-h] [-c COMPUTE] [-f FR] [-fa FR_ALL] [-l LOAD]

Compute graph

optional arguments:
  -h, --help            show this help message and exit
  -c COMPUTE, --compute COMPUTE
                        Compute graph of ASes from dump file
  -f FR, --fr FR        Compute graph of french ASes from dump file
  -fa FR_ALL, --frall FR_ALL
                        Compute graph of french ASes and foreign neighbor from dump file
  -l LOAD, --load LOAD  Load graph from graph file
```
