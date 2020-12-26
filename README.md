# [myNBA-Backend](https://boiling-shelf-26276.herokuapp.com)



MyNBA is a web app to that provides statistical analysis on the NBA using various machine learning models.

## Endpoints


### GET /GMMPred/kclusters
Generates labels based on Sklearn.GaussianMixture with `kclusters`.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `kclusters` | required | int  | Number of clusters for GMM.     
| 
**Response**

```

[
  {"class":0,"name":"Kyle Anderson"},..,{"class":0,"name":"OG Anunoby"},
  {"class":1,"name":"Domantas Sabonis"},...,{"class":1,"name":"Mason Plumlee"}
  {"class":2,"name":"Eric Bledsoe"},...,{"class":2,"name":"Trae Young"},
  {"class":3,"name":"Harrison Barnes"},...,{"class":3,"name":"Frank Kaminsky"}...
]
```
___


