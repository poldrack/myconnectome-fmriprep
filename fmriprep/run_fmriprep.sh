docker run -ti --rm \
    -v /data/ds000031:/data:ro \
    -v /data/ds000031/derivatives:/out \
    -v $FREESURFER_HOME/license.txt:/opt/freesurfer/license.txt \
    nipreps/fmriprep:22.0.2 \
    --fs-subjects-dir /out/freesurfer \
    --bids-filter-file /data/bids_filter.json \
    /data /out/fmriprep \
    participant 
