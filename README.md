# terraform-lambda-ebs-snapshots
AWS EBS Volume Backup &amp; Cleanup Terraform Module

## Introduction 

This module includes the necessary Terraform code to manage 2 Lambda functions to take backups of specified AWS EBS Volumes. It also can delete backups according to custom retention rules.

A lambda Terraform module, written by [sebolabs](https://github.com/sebolabs) has been included as a nested submodule.


## Usage
Information on how to use the module

### Example Config
### Snapshot Creation Lambda

```


```

You will need to create an SNS topic and subscribe yourself to it if you wish to recieve alerts on the failure of any specific Lambdas.
## Future Improvements


### Terraform Compatibility
