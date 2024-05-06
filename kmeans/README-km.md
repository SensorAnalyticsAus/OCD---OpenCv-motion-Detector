## NB This code is RaspberryPI OS specif

`../ctrl-cam01.sh start` and wait until at least 100  lines appear in `../log/MG.log`.

## Example

### Step 1 train
`python train-km.py 1 20 20230306000000 20230306235959` (these last two date-time args here will have to be changed to lie within your `MD.log` timeline)

### Step 2 predict (output frames from selected clusters from step 1)
`python predict-km.py 25`

### Step 3 create slideshow
`./moviefrm-list 30`
