# [myNBA-Backend](https://boiling-shelf-26276.herokuapp.com)

MyNBA is a web app to that provides statistical analysis on the NBA using various machine learning models.

## Endpoints


### GET /1/billing/retrieve-billing-data.json
Get basics billing data for the current user or for a given organization ID (as long as the current user is part of that organization). (it has been poorly implemented for now to unblock the Analyze team, and should only be used by Analyze) `official client only`

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `kclusters` | required | int  | Number of clusters for GMM.                                                                     |
|     
**Response**

```

[
  {"class":0,"name":"Kyle Anderson"},..,{"class":0,"name":"OG Anunoby"},
  {"class":1,"name":"Domantas Sabonis"},...,{"class":1,"name":"Domantas Sabonis"}
  {"class":2,"name":"Eric Bledsoe"},...,{"class":2,"name":"Trae Young"},
  {"class":3,"name":"Harrison Barnes"},...,{"class":3,"name":"Frank Kaminsky"}...
]
```
___


