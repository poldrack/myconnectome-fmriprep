# myconnectome-fmriprep

code/docs for running fmriprep on myconnectome

## Overall plan

1. process all anatomical directories using freesurfer 7.3.2, using -T2pial option if T2w is present (for use in subsequent longitudinal analysis in Freesurfer)
   - status: ongoing
2. create average field map for use in fMRIprep (following approach similar to that used in Laumann et al.)
   - status: TBD, need to decide whether to use phasediff or pepolar field maps
3. modify BIDS dataset to point to average field map for all BOLD datasets
   - status: need to figure out the necessary changes to BIDS metadata files
4. run fmriprep on a per-session basis

## Todos

## Mean field map generation:

*Original Laumann description:*: As field maps were not available for all sessions, a mean field
map was generated based on the available data. This mean field map was then applied to
all sessions for distortion correction. To generate the mean field map the following
procedure was used: (1) Poor quality field maps (4 out of 38) were excluded based on
visual inspection. (2) Field map magnitude images from selected sessions were mutually
co-registered. (3) Transforms between all sessions were resolved. Transform resolution
reconstructs the n-1 transforms between all images using the n*(n-1)/2 computed
transform pairs. (4) The resolved transforms were applied to generate a mean magnitude
image. (5) The mean magnitude image was registered to an atlas representative template.
(6) Individual session magnitude image to atlas space transforms were computed by
composing the session-to-mean and mean-to-atlas transforms. (7) Phase images were
then transformed to atlas space using the composed transforms, and a mean phase image
in atlas space was computed. 

*New procedure:*
- Two-stage procedure for registering images to common template
    - Stage 1: register all magnitude images to a common target (selected for good quality), and generate a mean of all registered images
    - Stage 2: register all magnitude images to Stage 1 mean image
- If using phasediff maps: Unwrap phase images using fsl PRELUDE
  - Check metadata to ensure that all field maps have same echo times
  - Apply Stage 2 transforms to phase images
  - Create mean registered phase image
- If using pepolar maps:
  - run topup (on individual or averaged acquisition?)
  - create mean fieldmap (or fieldmap of means?)