# PIPE-3955-NimbusBioImageTesting

This repository contains summary of Nimbus BioImage 2023-03 testing with a focus on sHPC, CVMFS, and Nextflow. 

## Command line examples

Tested examples provided in user guide for accessing CVMFS and sHPC, all worked well. 

Accessed Biocontainers cache fine:
```
ls -la /cvmfs/singularity.galaxyproject.org
```

Accessed Reference cache fine: 
```
ls -la /cvmfs/data.galaxyproject.org/
```

Using sHPC on the command line to explore biocontainers repository, checked how long it takes to module load a container: 
```
time module load quay.io/biocontainers/fastqc/0.12.1--hdfd78af_0/module

real    0m34.174s
user    0m31.762s
sys     0m2.595s
```

Rerun was fast: 
```
time module load quay.io/biocontainers/fastqc/0.12.1--hdfd78af_0/module

real    0m0.779s
user    0m0.745s
sys     0m0.034s
```

## nf-core/rnaseq 

Testing compatability Nextflow installation and sHPC modules with most recent version of the nf-core/rnaseq workflow v3.10.1.  

Checked version of Nextflow installed, as nf-core/rnaseq-3.10.1 requires >22.10.1: 
```
nextflow -version 

      N E X T F L O W
      version 22.10.7 build 5853
      created 18-02-2023 20:32 UTC 
      cite doi:10.1038/nbt.3820
      http://nextflow.io
```

Cloned repo for nf-core/rnaseq workflow: 
```
git clone https://github.com/nf-core/rnaseq.git
```

Download test data: 
```
wget -O nfcore_materials.tar.gz https://cloudstor.aarnet.edu.au/plus/s/gIBdDhKEwfq2j58/download
```

Unpack the files: 
```bash
tar -zxvf nfcore_materials.tar.gz
```

### Test run the default workflow without 

Test run workflow as we intend for exercise 2.1 of workshop: 
```
nextflow run rnaseq/main.nf --help 
```

Test run workflow in full:
```
materials=/home/ubuntu/nfcoreWorkshopTesting/materials/mm10_reference

nextflow run rnaseq/main.nf \
    --input ./materials/samplesheet.csv \
    --outdir /home/ubuntu/nfcoreWorkshopTesting/exercise1/results \
    --max_memory '6.GB' --max_cpus 2 \
    --gtf $materials/mm10_chr18.gtf \
    --fasta $materials/mm10_chr18.fa \
    --star_index $materials/STAR \
    -profile singularity \
    -with-report execution_report_exercise1.html \
    -with-trace execution_trace_exercise1.txt \
    -with-timeline timeline_exercise1.html \
    -with-dag dag_exercise1.png 
```

```
-[nf-core/rnaseq] Pipeline completed successfully-
WARN: Graphviz is required to render the execution DAG in the given format -- See http://www.graphviz.org for more info.
Completed at: 09-Mar-2023 06:36:50
Duration    : 18m 48s
CPU hours   : 0.4
Succeeded   : 202
```

### Cross-check biocontainers with nf-core/rnaseq config 

Downloaded Nandan's CVMFS config and make local copy to find requisite container names: 
```
wget -O working_directory.tar.gz https://cloudstor.aarnet.edu.au/plus/s/xveu7WCIdj7bk6c/download
tar -zxvf working_directory.tar.gz
cp working_directory/nextflow.config ./RNASEQ.config 
```

Extracted container names from `RNASEQ.config`:
```python
with open('RNASEQ.config', 'r') as file:
    for line in file:
        if 'container =' in line:
            container_path = line.split('/')[-1].strip(" '}\n")
            print(container_path)
```

Found 32 containers for 18 tools, multiple versions of MultiQC and Samtools: 
```
preseq-3.1.2--h06ef8b0_1.img'
python-3.8.3.img
python-3.8.3.img
python-3.8.3.img
python-3.8.3.img
python-3.8.3.img
stringtie-2.1.7--h978d192_0.img
subread-2.0.1--hed695b0_0.img
rseqc-3.0.1--py37h516909a_1.img
bioconductor-tximeta-1.8.0--r40_0.img
mulled-v2-cf0123ef83b3c38c13e3b0696a3f285d3f20f15b-606b713ec440e799d53a2b51a6e79dbfd28ecf3e-0.img
mulled-v2-8849acf39a43cdd6c839a369a74c0adc823e2f91-ab110436faf952a33575c64dd74615a84011450b-0.img
bbmap-38.93--he522d1c_0.img
bedtools-2.30.0--hc088bd4_0.img
multiqc-1.10.1--py_0.img
multiqc-1.11--pyhdfd78af_0.img
salmon-1.5.2--h84f40af_0.img
star-2.6.1d--0.img
fastqc-0.11.9--0.img
trim-galore-0.6.7--hdfd78af_0.img
qualimap-2.2.2d--1.img
picard-2.25.7--hdfd78af_0.img
ucsc-bedclip-377--h0b8a92a_2.img
ucsc-bedgraphtobigwig-377--h446ed27_1.img
samtools-1.13--h8c37831_0.img
samtools-1.10--h9402c20_2.img
samtools-1.13--h8c37831_0.img
samtools-1.13--h8c37831_0.img
samtools-1.13--h8c37831_0.img
samtools-1.13--h8c37831_0.img
bioconductor-dupradar-1.18.0--r40_1.img
bioconductor-summarizedexperiment-1.20.0--r40_0.img
```

Cross-check tools with those available through sHPC biocontainers:
```python
import subprocess

with open('RNASEQ.config', 'r') as file:
    tool_names = set()
    for line in file:
        if 'container =' in line:
            container_path = line.split("'")[1]
            tool_name = container_path.split('/')[-1].split('-')[0]
            tool_names.add(tool_name)
            #print(f'tool_name: {tool_name}')  # added line
    for tool_name in tool_names:
        command = ['shpc', 'show', '-f', 'quay.io/biocontainers/{}'.format(tool_name)]
        output = subprocess.check_output(command, text=True)
        expected_output = f'quay.io/biocontainers/{tool_name}'
        if output.strip() == expected_output:
            print(output.rstrip())
```

Extract correct versions, check with example (subread): 
```
module avail subread

---------------------------------------------------------------------- /home/ubuntu/singularity-hpc/modules ----------------------------------------------------------------------
   quay.io/biocontainers/bioconductor-rsubread/2.8.2--r41hc0cfd56_0/module    quay.io/biocontainers/subread/2.0.3--h7132678_1/module
```

Does not have required version (2.0.1)

## (Unsolicited) feedback on user guide 
* If possible would be useful to know what versions of pre-installed software is available  