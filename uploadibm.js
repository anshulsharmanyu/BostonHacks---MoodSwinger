const AWS = require('ibm-cos-sdk');

var config = {
    endpoint: 'https://s3.us-geo.objectstorage.softlayer.net',
    apiKeyId: 'XXXXXXXXXXXXXXX',
    ibmAuthEndpoint: 'https://iam.bluemix.net/oidc/token',
    serviceInstanceId: 'crn:v1:bluemix:public:cloud-object-storage:global:a/XXXXXXX:11111-as34-4b4d-3333-3334rfr4ed::',
};

var cos = new AWS.S3(config);


var params = {Bucket: 'downloadimages', Key: 'abcd.jpg', Body: 'abcd.jpg'};
cos.upload(params, function(err, data) {
  console.log(err, data);
});
