const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp();

exports.onMessageCreate = functions.firestore
    .document('messages/{userId}')
    .onCreate((snap, context) =>{
        const ref = admin.firestore().collection('messages').orderBy('timestamp');

        ref.onSnapshot(snapshot =>{
            i = 0;
            size = snpashot.size;
            sizeToDelete = size -10;
            console.log('Messages Count: ' + size);

            snapshot.forEach((doc) => {
                if(i < sizeToDelete){
                    doc.ref.delete().then(() =>{
                        console.log("Document deleted successfully");
                    }).catch((error)=>{
                        console.log("Error removing document " + error);
                    });
                }
                i++;
            });
        });
    });
// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
