# VizSense

Write something about vizsense

## Installation

Use the bellow bash scrip to install **VizSense** Tool.
Please create a file *vizsense-setup.sh* ,And provide excution permission using bellow command -:  
*sudo chmod -R +x vizsense-setup.sh*  
 Then run -:  *sh vizsense-setup.sh*
  
```bash
#!/bin/bash
#vim vizsense-setup.sh

workdir()
{
"cd" vizsense
sudo docker-compose build
kubectl apply -f deployment
kubectl apply -f deployment/keda
kubectl apply -f deployment/services
}
read -p "Please enter the branch name or hit enter to continue with default branch: " branch
read -p "Please provide User Name like shivendratiwari10: " user
read -p "Please provide Personal access token like ghp_v3UVMgdVncdRt9GJfghjkfICD778X536XOCC: " tocken


if [ $branch == ""]
then
  echo "clonning default branch........."
  git clone https://$user:$tocken@github.com/GathiAnalytics/vizsense.git
  echo "cloned successfully............Enjoy"
  workdir
else
  echo "cloning branch $branch"
  git clone https://$user:$tocken@github.com/GathiAnalytics/vizsense.git --branch $branch
  echo "successfully cloned branch $branch"
  workdir

fi

```
Note :- This script will only work if, k8s Cluster is Up and Running,
So Please make sure having a Healthy k8s cluster
## Usage

Write the uses of VizSense


## Contributing
Write something about the contribution
## License
[Apexon](https://www.apexon.com/)
