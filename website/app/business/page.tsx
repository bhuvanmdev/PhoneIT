"use client";
import React, { useState } from "react";
import { db, storage } from "../firebase";
import { collection, addDoc } from "firebase/firestore";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import Image from "next/image";
import { toast } from "react-toastify";

const Page = () => {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    business: "",
    context: "",
    file: null,
  } as {
    name: string;
    
    phone: string;
    business: string;
    context: string;
    file: any;});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, files } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (
      formData.name &&
      formData.phone &&
      formData.business &&
      formData.context &&
      formData.file
    ) {
      try {
        let fileURL = "";

        if (formData.file) {
            const fileRef = ref(storage, `files/${formData.file.name}`);
            await uploadBytes(fileRef, formData.file);
            fileURL = await getDownloadURL(fileRef);
        }

        const docRef = await addDoc(collection(db, "messages"), {
            name: formData.name,
            phone: formData.phone,
            business: formData.business,
            context: formData.context,
            fileURL,
        });

        console.log("Document written with ID: ", docRef.id);

        setFormData({
          name: "",
          phone: "",
          business: "",
          context: "",
          file: null,
        });
      } catch (e) {
        toast.error("Error adding document");
      }
    } else {
      toast.warn("Please fill in all fields", { autoClose: 2000 });
    }
  };

  return (
    <div className="flex min-h-screen flex-col gap-4 p-24">
      <h1 className="text-5xl">Create your own agent</h1>
      <p>Send us a message to help you setup your own business</p>
      <div className="flex">
        <form
          className="flex flex-col gap-4 w-1/2 mt-8"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            className="p-4 bg-black border-b-2"
          />
          <input
            type="number"
            name="phone"
            placeholder="Phone Number"
            value={formData.phone}
            onChange={handleChange}
            className="p-4 bg-black border-b-2"
          />
          <input
            type="text"
            name="business"
            placeholder="Business"
            value={formData.business}
            onChange={handleChange}
            className="p-4 bg-black border-b-2"
          />
          <input
            name="context"
            type="textarea"
            placeholder="Context"
            value={formData.context}
            onChange={handleChange}
            className="p-4 bg-black border-b-2"
          />
          <input
            type="file"
            name="file"
            onChange={handleChange}
            className="p-4"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white p-4 rounded-lg"
          >
            Send Message
          </button>
        </form>
        <div className="w-1/2 flex items-center justify-center">
          <Image
            src="/telephone.png"
            width={250}
            height={250}
            alt="contact-us-logo"
          />
        </div>
      </div>
    </div>
  );
};

export default Page;
