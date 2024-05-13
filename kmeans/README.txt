Example

Step 1 train
/path/to/.venv/bin/python train-km.py 1 10 20230306000000 20230306235959

Step 2 predict (output frames from selected clusters from step 1)
/path/to/.venv/bin/python predict-km.py 80

Step 3 create slideshow
./moviefrm-list 30 
