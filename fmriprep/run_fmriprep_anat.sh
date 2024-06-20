docker run -ti --rm \
    -v /data/ds000031:/data:ro \
    -v /data/ds000031/derivatives:/out \
    -v $FREESURFER_HOME/license.txt:/opt/freesurfer/license.txt \
    nipreps/fmriprep:22.0.2 \
    --anat-only \
    /data /out/fmriprep \
    participant 
