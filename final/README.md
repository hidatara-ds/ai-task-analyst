# report generation and AI helper

#### This is an implementation of a friendly way to query a database, which contains the data retrieved from am AI chatbot.

I used **FastAPI** for this implementation because of its async nature.

---

There was a need to generate reports monthly using SQL. However, the people that work for the chatbot startup don't really know how to interact with databases.

So, i created a simple API to help them retrieve and export the data that they want.

---

Also, i created an AI workflow, which creates brand new queries to get the data needed to answer the user question.

After getting the data, some insights are generated based on the results and user prompt.

---

There is also a really simple frontend to interact with the AI workflow, but that's not the focus of the app.

The users will be interacting directly with the FastAPI swagger, which i believe it very usefull in scenarios like this, when you're only going to use the tool internally and don't have many routes.

---

The following print screen is from the page where the users can interact with the SQL agent:

![report_generation](https://github.com/user-attachments/assets/242fd10a-5a3e-4843-b433-35b87cabf46e)
