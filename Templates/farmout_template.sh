#!/bin/bash
# This script was created at ${time} with the command: 
#     ${command}
#
# To resubmit failed jobs: ./farmout.sh --resubmit-failed-jobs
pushd ${base_dir}
tar \
    -zcvf ${job_dir}/analysis_code.tar.gz \
    Cuts/ \
    Utilities/ \
    skimNtuples.py
./Utilities/scripts/makeInputFilesList.py \
    -o ${job_dir}/input_file_list.txt \
    -p ${input_files_path}
popd
chmod +x ${job_dir}/skim.sh
farmoutAnalysisJobs \
    --infer-cmssw-path \
    --fwklite \
    --input-file-list=${job_dir}/input_file_list.txt \
    --submit-dir=${job_dir}/submit \
    --input-files-per-job=${files_per_job} \
    --input-dir=root://cmsxrootd.hep.wisc.edu/ \
    --assume-input-files-exist \
    --extra-inputs=${job_dir}/analysis_code.tar.gz \
    $$1 \
    ${job_name} \
    ${job_dir}/skim.sh
