// front/src/lib/firebase.js

import { initializeApp, getApps } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";

// Read from Vite envs; leave blank if not configured yet
const firebaseConfig = {
  apiKey:            import.meta.env.VITE_FIREBASE_API_KEY || "",
  authDomain:        import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "",
  projectId:         import.meta.env.VITE_FIREBASE_PROJECT_ID || "",
  storageBucket:     import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "",
  appId:             import.meta.env.VITE_FIREBASE_APP_ID || "",
};

// Only init if we actually have a projectId (keeps Firebase optional for now)
let app = null;
let db = null;
let storage = null;

if (firebaseConfig.projectId) {
  app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);
  db = getFirestore(app);
  storage = getStorage(app);
}

/**
 * Upload an image file to Firebase Storage and return a public download URL.
 * @param {File|Blob} file
 * @param {string} pathPrefix folder path prefix (default: "products")
 * @returns {Promise<string>} download URL
 */
export async function uploadImageAndGetURL(file, pathPrefix = "products") {
  if (!app || !storage) {
    throw new Error(
      "Firebase is not configured. Set VITE_FIREBASE_* envs (including VITE_FIREBASE_STORAGE_BUCKET)."
    );
  }
  const safeName = (file?.name || "image").replace(/[^\w.-]/g, "_");
  const objectPath = `${pathPrefix}/${Date.now()}_${safeName}`;
  const objectRef = ref(storage, objectPath);
  await uploadBytes(objectRef, file);
  return await getDownloadURL(objectRef);
}

export { app, db, storage };

