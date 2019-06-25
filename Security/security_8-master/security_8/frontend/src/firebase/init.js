import firebase from "firebase";

var firebaseConfig = {
  apiKey: "AIzaSyDgMX8f2KD5DJUJlatTJIgsFIsJxB97suQ",
  authDomain: "vuejs-firebase-01-7f17a.firebaseapp.com",
  databaseURL: "https://vuejs-firebase-01-7f17a.firebaseio.com",
  projectId: "vuejs-firebase-01-7f17a",
  storageBucket: "vuejs-firebase-01-7f17a.appspot.com",
  messagingSenderId: "624914407418",
  appId: "1:624914407418:web:c34604cc8060e05b"
};
// Initialize Firebase
const firebaseApp = firebase.initializeApp(firebaseConfig);
firebaseApp.firestore().settings({ timestampsInSnapshots: true });

export default firebaseApp.firestore();
