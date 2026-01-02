// Import the functions you need from the SDKs you need
import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBDzHESAOmCytbVvibQ9NCd_gn5-WBRszQ",
  authDomain: "realtime-smart-vision.firebaseapp.com",
  databaseURL: "https://realtime-smart-vision-default-rtdb.firebaseio.com",
  projectId: "realtime-smart-vision",
  storageBucket: "realtime-smart-vision.firebasestorage.app",
  messagingSenderId: "500348017645",
  appId: "1:500348017645:web:a754af3e1676e1e50e25e4",
  measurementId: "G-BZD78VFEM4"
};

// Initialize Firebase
let app;
if (getApps().length === 0) {
    app = initializeApp(firebaseConfig);
    console.log("Firebase initialized on client side");
} else {
    app = getApps()[0];
    console.log("Firebase already initialized, using existing app");
}

const analytics = getAnalytics(app);

export { app, analytics };
