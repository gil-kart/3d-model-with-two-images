# 3d-model-with-two-images
given two images of the same scene, taken from different angle, create a 3d model of the objects that appear in the images

so let's take a look at this two images of a house:

![house_1](https://user-images.githubusercontent.com/73134488/181602906-6a9796b4-a147-44d8-b86c-2f33a2abda23.png)
![house_2](https://user-images.githubusercontent.com/73134488/181603103-a912f0b2-b9e3-4c06-a580-38c1f5c3257a.png)

it's the same house but from two different angles. 
what we want to do is create a 3d model of the house. 
the way we're going to do it is by marking matching points on both of the images:

![house1_points](https://user-images.githubusercontent.com/73134488/181607430-a1c6d6d0-c302-4513-93d1-e23974db8f60.jpg)
![house2_points](https://user-images.githubusercontent.com/73134488/181607497-457b0336-845a-449b-89d2-4e0ad96250c5.jpg)

now, using the camera matrix of each image, and the two lists of matching points, we use Direct Linear Transformation algorithm to get a point in a 3d space.

this is how the 3d points look when only looking at the x and y axis:
![3d_points](https://user-images.githubusercontent.com/73134488/181612561-fca26bb3-c4ec-4913-8d02-c9bce020e416.jpg)

now from each point, we draw a line to the next point at the list so we get a nice house model:

![house_model](https://user-images.githubusercontent.com/73134488/181612910-76c7c5c3-1309-4354-9250-36052291d0ba.jpg)


and this is how the model looks when performing rotation transformation on it:
![output_gif](https://user-images.githubusercontent.com/73134488/181613002-c00e92cb-4547-4b30-bf6a-eb93e5d5893b.gif)

so now, for every two images of an object, showen from two different angles, we can create a model of it, by marking matching points. the model will look more accurate when using a larger number of points. 

