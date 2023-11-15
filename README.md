# Micla_docs

ok my plan is to get teh automation working next I want the automation to work when I make some changes and then push into main 
this should push to a new branch named docs or something 

after that I need to sort out the TODO issues in the make.py file after that I need to implement it into twinlab

I currently have workflow that 
1. copies the docs folder from the branch it has been pushed
2. replaces the docs folder in the docs_deployment branch with the new docs folder 

I now want to
1. Add the pdoc thing that actually updates from the documentation of my fake modules 
2. Figure out if I actually also need to run a mkdocs command in all of this 
3. make the same changes form here in twinlab by branches off of Alexanders branch 
   

WARNING: when doing the thing in twinlab some issues may arries because I am not sure if you are allowed to use a workflow to push, to get arround this we might either have to work with Github secrets or change the allowences of what the github workflows are allowed to do in settings

TODO: I also should do some manual testings to see if things are changed manually or pushed in the wromg order you get issues 

1. try with a pull request 

Doing the same thing with twinlab ... I have now tried to get it to work with twinlab I assume the reason it doesn't work is that pdoc works in a bad way and has to import all the libraries for it to work so it will only work from the folder twinlab is actually in .. maybe this is not the best way of going around it but I could move the python script inside of client and try testing it 

next steps: 
1. sort out this docs folder that I have -- DONE 
2. delete the files I don't need including make.py -- DONE
3. put it into thw root directory of twinlab  -- DONE
4. make sure the twinlab files are shown and it all looks good on the website if you call mkdocs serve -- DONE
5. edit the workflow to run the new python file to update the documentation 
6. Make a new branch that contains a new version of the docs folder and branches off of dev, use the new checkout method to copy one folder to make this work --DONE
7. to get Further understnading try taking out the working directoy bit and pwd what happened?[] (I didn't do this for now becuse I am just working in client/python)
8. Re-structure the .yml file to call the make.py from the client/python directory and also to push and pull the right things since the directory we are working in has changed --DONE
9. Fix problem with twinlab import by poetry installing
10. sort out the fixes with permission and stuff from above [] (this should be fine but it should be)
11. decide if I should install pdoc with pip or poetry (probably poetry from what has happened so far)


8. We should do something about the documentation for instalation inside the python does not get removed but we will figure that out
9. I think the python should have 3 folders inside of it: - the docs explaining the folders, -installation documentation - notebooks (maybe this should also be split into 2 as in guides and examples but I am not actually sure since it will porbably just be links for now)
10. figure out what the set up cache step actually does

N.B if we end up putting the jupyternotebooks as links add as a task to the backlog to find a diffrent option 

3:45 current status: 
    - working github workflow in my repo 
    - working python script that reads form twinlab with pdocs
- coninue from step 6 
