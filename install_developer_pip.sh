pip show testinfrastructure;ret=$? 
if [ $ret -eq 0 ]; then
    echo "allredy installed"
else 
    pip install -e git+https://github.com/MPIBGC-TEE/testinfrastructure.git#egg=testinfrastructure
fi 
    pip install -e .  
