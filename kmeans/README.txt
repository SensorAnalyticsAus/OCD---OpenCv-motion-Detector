Example

Step 1 train
python train-km.py 1 20 20230306000000 20230306235959

Step 2 predict (output frames from selected clusters from step 1)
python predict-km.py 25

Step 3 create slideshow
./moviefrm-list 30 
