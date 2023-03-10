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
All ran well in expected time:
```
-[nf-core/rnaseq] Pipeline completed successfully-
WARN: Graphviz is required to render the execution DAG in the given format -- See http://www.graphviz.org for more info.
Completed at: 09-Mar-2023 06:36:50
Duration    : 18m 48s
CPU hours   : 0.4
Succeeded   : 202
```

### Cross-check biocontainers with nf-core/rnaseq config 

Software version are output by pipeline after a successful run, checked them (`results/pipeline_info/software_versions.yml`):
```yaml
BEDTOOLS_GENOMECOV:
  bedtools: 2.30.0
CUSTOM_DUMPSOFTWAREVERSIONS:
  python: 3.10.6
  yaml: '6.0'
CUSTOM_GETCHROMSIZES:
  getchromsizes: 1.16.1
DESEQ2_QC_STAR_SALMON:
  bioconductor-deseq2: 1.28.0
  r-base: 4.0.3
DUPRADAR:
  bioconductor-dupradar: 1.28.0
  r-base: 4.2.1
FASTQC:
  fastqc: 0.11.9
GTF2BED:
  perl: 5.26.2
GTF_GENE_FILTER:
  python: 3.9.5
MAKE_TRANSCRIPTS_FASTA:
  rsem: 1.3.1
  star: 2.7.10a
MULTIQC_CUSTOM_BIOTYPE:
  python: 3.9.5
PICARD_MARKDUPLICATES:
  picard: 2.27.4-SNAPSHOT
QUALIMAP_RNASEQ:
  qualimap: 2.2.2-dev
RSEQC_BAMSTAT:
  rseqc: 3.0.1
RSEQC_INFEREXPERIMENT:
  rseqc: 3.0.1
RSEQC_INNERDISTANCE:
  rseqc: 3.0.1
RSEQC_JUNCTIONANNOTATION:
  rseqc: 3.0.1
RSEQC_JUNCTIONSATURATION:
  rseqc: 3.0.1
RSEQC_READDISTRIBUTION:
  rseqc: 3.0.1
RSEQC_READDUPLICATION:
  rseqc: 3.0.1
SALMON_INDEX:
  salmon: 1.9.0
SALMON_QUANT:
  salmon: 1.9.0
SALMON_SE_GENE:
  bioconductor-summarizedexperiment: 1.24.0
  r-base: 4.1.1
SALMON_TX2GENE:
  python: 3.9.5
SALMON_TXIMPORT:
  bioconductor-tximeta: 1.12.0
  r-base: 4.1.1
SAMPLESHEET_CHECK:
  python: 3.9.5
SAMTOOLS_FLAGSTAT:
  samtools: 1.16.1
SAMTOOLS_IDXSTATS:
  samtools: 1.16.1
SAMTOOLS_INDEX:
  samtools: 1.16.1
SAMTOOLS_SORT:
  samtools: 1.16.1
SAMTOOLS_STATS:
  samtools: 1.16.1
STAR_ALIGN:
  gawk: 5.1.0
  samtools: 1.16.1
  star: 2.7.9a
STRINGTIE_STRINGTIE:
  stringtie: 2.2.1
SUBREAD_FEATURECOUNTS:
  subread: 2.0.1
TRIMGALORE:
  cutadapt: '3.4'
  trimgalore: 0.6.7
UCSC_BEDCLIP:
  ucsc: '377'
UCSC_BEDGRAPHTOBIGWIG:
  ucsc: '377'
Workflow:
  Nextflow: 22.10.7
  nf-core/rnaseq: 3.10.1
``` 

Cross-check tools and versions with those available through sHPC biocontainers:
```python
import re
import subprocess

with open("results/pipeline_info/software_versions.yml", "r") as f:
    lines = f.readlines()
    for line in lines:
        match = re.match(r"^(\b\w+\b):\s*\d+\.\d+\.\d+$", line.strip())
        if match:
            toolname = match.group(1)
            if not toolname.startswith(('python-', 'perl-')):
                command = f"shpc show --versions -f quay.io/biocontainers/{toolname}"
                output = subprocess.check_output(command, shell=True, text=True).strip()
                versions = set()
                for tool in output.split('\n'):
                    if not tool.startswith(('quay.io/biocontainers/python-', 'quay.io/biocontainers/python_','quay.io/biocontainers/perl-')):
                        versions.add(tool.strip())
                if versions:
                    print(f"{toolname}: {', '.join(versions)}")
```
```
bedtools: quay.io/biocontainers/bedtools:2.30.0--h468198e_3
python: quay.io/biocontainers/python:3.9, quay.io/biocontainers/python:3.10, quay.io/biocontainers/python:3, quay.io/biocontainers/python:3.9--1
getchromsizes: 
fastqc: quay.io/biocontainers/fastqc:0.11.9--hdfd78af_1, quay.io/biocontainers/fastqc-rs:0.3.2--he9f29cb_1, quay.io/biocontainers/fastqc:0.11.9--0
perl: quay.io/biocontainers/perl:5.26.2, quay.io/biocontainers/perl:5.26
python: quay.io/biocontainers/python:3.9, quay.io/biocontainers/python:3.10, quay.io/biocontainers/python:3, quay.io/biocontainers/python:3.9--1
rsem: quay.io/biocontainers/rsem:1.3.3--pl5321h6b7c446_6, quay.io/biocontainers/rsem:1.3.3--pl5321ha04fe3b_5
python: quay.io/biocontainers/python:3.9, quay.io/biocontainers/python:3.10, quay.io/biocontainers/python:3, quay.io/biocontainers/python:3.9--1
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
rseqc: quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0, quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2
salmon: quay.io/biocontainers/salmon:1.7.0--h10bb6b4_1, quay.io/biocontainers/salmon:1.8.0--h7e5ed60_1, quay.io/biocontainers/salmon:1.6.0--h84f40af_0, quay.io/biocontainers/salmon:1.5.2--h84f40af_0, quay.io/biocontainers/salmon:1.4.0--h84f40af_1, quay.io/biocontainers/salmon:1.9.0--h7e5ed60_1
salmon: quay.io/biocontainers/salmon:1.7.0--h10bb6b4_1, quay.io/biocontainers/salmon:1.8.0--h7e5ed60_1, quay.io/biocontainers/salmon:1.6.0--h84f40af_0, quay.io/biocontainers/salmon:1.5.2--h84f40af_0, quay.io/biocontainers/salmon:1.4.0--h84f40af_1, quay.io/biocontainers/salmon:1.9.0--h7e5ed60_1
python: quay.io/biocontainers/python:3.9, quay.io/biocontainers/python:3.10, quay.io/biocontainers/python:3, quay.io/biocontainers/python:3.9--1
python: quay.io/biocontainers/python:3.9, quay.io/biocontainers/python:3.10, quay.io/biocontainers/python:3, quay.io/biocontainers/python:3.9--1
samtools: quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.13--h8c37831_0, quay.io/biocontainers/samtools:1.11--h6270b1f_0
samtools: quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.13--h8c37831_0, quay.io/biocontainers/samtools:1.11--h6270b1f_0
samtools: quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.13--h8c37831_0, quay.io/biocontainers/samtools:1.11--h6270b1f_0
samtools: quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.13--h8c37831_0, quay.io/biocontainers/samtools:1.11--h6270b1f_0
samtools: quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.13--h8c37831_0, quay.io/biocontainers/samtools:1.11--h6270b1f_0
gawk: quay.io/biocontainers/gawk:5.1.0
samtools: quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.13--h8c37831_0, quay.io/biocontainers/samtools:1.11--h6270b1f_0
stringtie: quay.io/biocontainers/stringtie:2.2.1--hecb563c_2
subread: quay.io/biocontainers/subread:2.0.1--h7132678_2, quay.io/biocontainers/subread:2.0.3--h7132678_0, quay.io/biocontainers/subread:2.0.3--h7132678_1
trimgalore: 
Nextflow: 
```

## (Unsolicited) feedback on user guide 
* If possible would be useful to know what versions of pre-installed software is available  