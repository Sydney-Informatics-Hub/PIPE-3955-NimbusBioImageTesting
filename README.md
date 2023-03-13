# PIPE-3955-NimbusBioImageTesting

This repository contains summary of Nimbus BioImage 2023-03 testing with a focus on sHPC, CVMFS, RStudio, and Nextflow. 

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

## nf-core/rnaseq and sHPC

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
```bash
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
    results = []
    for line in lines:
        match = re.match(r"^(\b\w+-?\w*\b|\b\w+\s\w+\b):\s*(['\"]?[\d.]+[a-z-]*['\"]?)$", line.strip())
        if match:
            toolname = match.group(1)
            if not toolname.startswith(('python-', 'perl-')):
                command = f"shpc show --versions -f quay.io/biocontainers/{toolname}"
                output = subprocess.check_output(command, shell=True, text=True).strip()
                versions = set()
                for tool in output.split('\n'):
                    if not tool.startswith(('quay.io/biocontainers/star-', 'quay.io/biocontainers/python-', 'quay.io/biocontainers/python_','quay.io/biocontainers/perl-')):
                        versions.add(tool.strip())
                if versions:
                    version_str = ', '.join(versions)
                    # Get the version of the tool from the YAML file
                    version_match = re.search(rf"{toolname}:\s*([\d\.]+)", "".join(lines))
                    version = version_match.group(1) if version_match else None
                    # Append the tool name and its version to the results list
                    results.append(f"{toolname}/{version}: {version_str}")
    # Sort and deduplicate the results
    results = sorted(set(results))
    for result in results:
        print(result)
```
Found a few nf-core/rnaseq tools that either didn't match versions or weren't available on sHPC: 

* deseq2/1.28.0: 1.34.0
* getchromsize/1.16.1: none 
* python/3.10/6: 3.10
* rsem/1.3.1: 1.3.3
* rseqc/3.0.1: 4.0.0
* samtools/1.16: 1.15 
* star/2.7.10: 2.7.1a
* trimgalore/0.6.7: none

Additionally, despite being able to see multiple versions of tools available on sHPC, not all have module files and therefore cannot be used. 

```
bedtools/2.30.0: quay.io/biocontainers/bedtools:2.30.0--h468198e_3
bioconductor-deseq2/1.28.0: quay.io/biocontainers/bioconductor-deseq2:1.34.0--r41hc247a5b_3, quay.io/biocontainers/bioconductor-deseq2:1.38.0--r42hc247a5b_0
bioconductor-dupradar/1.28.0: quay.io/biocontainers/bioconductor-dupradar:1.20.0--r40hdfd78af_1, quay.io/biocontainers/bioconductor-dupradar:1.18.0--r40_1, quay.io/biocontainers/bioconductor-dupradar:1.24.0--r41hdfd78af_0, quay.io/biocontainers/bioconductor-dupradar:1.8.0--r3.4.1_1, quay.io/biocontainers/bioconductor-dupradar:1.22.0--r41hdfd78af_0, quay.io/biocontainers/bioconductor-dupradar:1.28.0--r42hdfd78af_0
bioconductor-summarizedexperiment/1.24.0: quay.io/biocontainers/bioconductor-summarizedexperiment:1.22.0--r41hdfd78af_0, quay.io/biocontainers/bioconductor-summarizedexperiment:1.28.0--r42hdfd78af_0, quay.io/biocontainers/bioconductor-summarizedexperiment:1.24.0--r41hdfd78af_0, quay.io/biocontainers/bioconductor-summarizedexperiment:1.18.1--r40_0, quay.io/biocontainers/bioconductor-summarizedexperiment:1.20.0--r40hdfd78af_1, quay.io/biocontainers/bioconductor-summarizedexperiment:1.8.0--r3.4.1_0
bioconductor-tximeta/1.12.0: quay.io/biocontainers/bioconductor-tximeta:1.8.4--r40hdfd78af_0, quay.io/biocontainers/bioconductor-tximeta:1.16.0--r42hdfd78af_0, quay.io/biocontainers/bioconductor-tximeta:1.12.0--r41hdfd78af_0, quay.io/biocontainers/bioconductor-tximeta:1.14.0--r41hdfd78af_0, quay.io/biocontainers/bioconductor-tximeta:1.10.0--r41hdfd78af_0
cutadapt/None: quay.io/biocontainers/cutadapt:3.5--py39h38f01e4_0, quay.io/biocontainers/cutadapt:3.7--py38hbff2b2d_0, quay.io/biocontainers/cutadapt:3.4--py38h4a8c8d9_1
fastqc/0.11.9: quay.io/biocontainers/fastqc:0.11.9--hdfd78af_1, quay.io/biocontainers/fastqc-rs:0.3.2--he9f29cb_1, quay.io/biocontainers/fastqc:0.11.9--0
gawk/5.1.0: quay.io/biocontainers/gawk:5.1.0
getchromsizes/1.16.1: 
perl/5.26.2: quay.io/biocontainers/perl:5.26, quay.io/biocontainers/perl:5.26.2
python/3.10.6: quay.io/biocontainers/python:3.10, quay.io/biocontainers/pythonnet:2.3.0--py27_1, quay.io/biocontainers/pythonpy:0.4.11--py_0, quay.io/biocontainers/python:3, quay.io/biocontainers/python:3.9, quay.io/biocontainers/python:3.9--1, quay.io/biocontainers/pythonpy:0.4.2--py_1
qualimap/2.2.2: quay.io/biocontainers/qualimap:2.2.2a--2, quay.io/biocontainers/qualimap:2.2.2d--hdfd78af_2
r-base/4.0.3: quay.io/biocontainers/r-basejump:0.11.23--r36_0, quay.io/biocontainers/r-base64:1.1--r3.2.2_0, quay.io/biocontainers/r-basejump:0.10.9--r351_1, quay.io/biocontainers/r-basejump:0.12.16--r40_0, quay.io/biocontainers/r-basejump:0.13.4--r40_0, quay.io/biocontainers/r-base:4.2.1, quay.io/biocontainers/r-basejump:0.9.9--r351_0, quay.io/biocontainers/r-basejump:0.14.17--r41hdfd78af_2
rsem/1.3.1: quay.io/biocontainers/rsem:1.3.3--pl5321h6b7c446_6, quay.io/biocontainers/rsem:1.3.3--pl5321ha04fe3b_5
rseqc/3.0.1: quay.io/biocontainers/rseqc:4.0.0--py36h91eb985_2, quay.io/biocontainers/rseqc:5.0.1--py310h1425a21_0
salmon/1.9.0: quay.io/biocontainers/salmon:1.4.0--h84f40af_1, quay.io/biocontainers/salmon:1.6.0--h84f40af_0, quay.io/biocontainers/salmon:1.7.0--h10bb6b4_1, quay.io/biocontainers/salmon:1.9.0--h7e5ed60_1, quay.io/biocontainers/salmon:1.8.0--h7e5ed60_1, quay.io/biocontainers/salmon:1.5.2--h84f40af_0
samtools/1.16.1: quay.io/biocontainers/samtools:1.11--h6270b1f_0, quay.io/biocontainers/samtools:1.12--h9aed4be_1, quay.io/biocontainers/samtools:1.15--h3843a85_0, quay.io/biocontainers/samtools:1.10--h2e538c0_3, quay.io/biocontainers/samtools:1.14--hb421002_0, quay.io/biocontainers/samtools:1.13--h8c37831_0
star/2.7.10: quay.io/biocontainers/staramr:0.8.0--pyhdfd78af_1, quay.io/biocontainers/stare-abc:1.0.3.1--h72a8191_0, quay.io/biocontainers/start-asap:1.3.0--hdfd78af_1, quay.io/biocontainers/starcode:1.4--hec16e2b_2, quay.io/biocontainers/star:2.7.10a--h9ee0642_0, quay.io/biocontainers/stark:0.1.1--h9f5acd7_3, quay.io/biocontainers/starseqr:0.6.7--py39h5371cbf_4, quay.io/biocontainers/starfish:0.2.2--pyhdfd78af_0, quay.io/biocontainers/staramr:0.9.1--pyhdfd78af_0
stringtie/2.2.1: quay.io/biocontainers/stringtie:2.2.1--hecb563c_2
subread/2.0.1: quay.io/biocontainers/subread:2.0.3--h7132678_1, quay.io/biocontainers/subread:2.0.3--h7132678_0, quay.io/biocontainers/subread:2.0.1--h7132678_2
trimgalore/0.6.7: 
ucsc/None: quay.io/biocontainers/ucsc-cell-browser:1.1.1--pyhdfd78af_1
yaml/None: quay.io/biocontainers/yamllint:1.2.1--py36_0
```

## Test nf-core/rnaseq with sHPC config file

Tested use of different version of STAR in `sHPC.config`:
```
// test profile for Nimbus BioImage + sHPC

// Replace STAR container with sHPC module
process {
    withName: 'BEDTOOLS_GENOMECOV'  { module = 'quay.io/biocontainers/bedtools/2.30.0--h468198e_3/module' }
    withName: 'FASTQC'              { module = 'quay.io/biocontainers/fastqc/0.12.1--hdfd78af_0/module' }
    withName: 'QUALIMAP_RNASEQ'     { module = 'quay.io/biocontainers/qualimap/2.2.2d--hdfd78af_2/module' }
    withName: 'STAR_ALIGN'          { module = 'quay.io/biocontainers/star/2.7.9a--h9ee0642_0/module' }
    withName: 'RSEQC_BAMSTAT | RSEQC_INFEREXPERIMENT | RSEQC_INNERDISTANCE | RSEQC_JUNCTIONANNOTATION | RSEQC_JUNCTIONSATURATION | RSEQC_READDISTRIBUTION | RSEQC_READDUPLICATION' { module = 'quay.io/biocontainers/rseqc/5.0.1--py39hbf8eff0_0/module' } 
    withName: 'SALMON_INDEX | SALMON_QUANT' { module = 'quay.io/biocontainers/salmon/1.9.0--h7e5ed60_1/module' }   
    withName: 'STRINGTIE_STRINGTIE' { module = 'quay.io/biocontainers/stringtie/2.2.1--ha04fe3b_3/module' }
}
```

Re-ran workflow: 
```
materials=/home/ubuntu/PIPE-3955-NimbusBioImageTesting/materials/mm10_reference/

nextflow run rnaseq/main.nf \
    --input ./materials/samplesheet.csv \
    --outdir /home/ubuntu/nfcoreWorkshopTesting/sHPC/results \
    --max_memory '6.GB' --max_cpus 2 \
    --gtf $materials/mm10_chr18.gtf \
    --fasta $materials/mm10_chr18.fa \
    --star_index $materials/STAR \
    -profile singularity \
    -config sHPC.config \ 
    -with-report execution_report_sHPC2.html \
    -with-trace execution_trace_sHPC2.txt \
    -with-timeline timeline_sHPC2.html \
    -with-dag dag_sHPC2.png 
```

Replacing container with sHPC module for process works and workflow runs to completion. 
```
-[nf-core/rnaseq] Pipeline completed successfully-
Completed at: 13-Mar-2023 04:37:11
Duration    : 17m 2s
CPU hours   : 0.5
Succeeded   : 202
```

## Questions and (unsolicited) feedback 
* Would be useful to know what versions of pre-installed software is available in BioImage documentation/user guide
* Am I able to access all biocontainers with sHPC on Nimbus? 
  * Example: STAR does not have current version, despite more recent versions being [available on quay.io/biocontainers](https://quay.io/repository/biocontainers/star?tab=tags)
* Is it possible for me (or anyone?) to create or request a module file be created for versions not currently available?  