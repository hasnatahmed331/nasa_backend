
# Open Science Project Marketplace

## Challenge: Building a Marketplace for Open Science Projects
Nasa Space Apps Challenge 2023

### `Front End Reposiroy`
Click here to See Backend Repository : React [Front-End Code](https://github.com/tareeb/OpenSourcerers) 

### Project Name : 
#### OpenSourcerers
A place where Everyone can show  Magic of their Open Source

### Objective
The goal of this project is to create a platform that facilitates the connection between creators of open science projects and skilled contributors by improving upon traditional tag-based systems.

### Problem Statement
Traditional tag-based systems tend to deteriorate over time as they rely on strict equality and a finite number of predefined tags. Managing a vast number of tags in a large system can become unwieldy and challenging to keep up to date.

### Our Solution: Semantic-Based Search
Our approach employs semantic-based search using a vector database to store vector embeddings of project descriptions and user bios. This system enables project creators and collaborators to discover each other through four different methods:

1. **Project Collaborators can search for projects by describing the project they want to work on.**
2. **Project Collaborators can receive project recommendations based on their bios.**
3. **Project creators can search for collaborators by describing the desired bios for their projects.**
4. **Project creators can receive collaborator recommendations based on their project descriptions.**

### Benefits of Our Solution
1. **Semantic Search:** The system offers semantic search capabilities, going beyond simple tags.
2. **Context Awareness:** It generates context-aware results, allowing for infinite contextual tags.
3. **Advanced Matching:** The system considers expertise, similarity, and more, going beyond traditional tag-based systems.

### Example Illustrating the System's Superiority Over Traditional Tags
Suppose we have several developers' bios in the database, including web developers with different specializations:

1. Developer A: Front-end expert with React experience.
2. Developer B: Backend specialist with extensive experience in financial systems.
3. Developer C: General web developer with a recent experience in creating learning management systems (LMS) for a school.

If a project description mentions the need for an expert web developer for an e-learning platform, our system would prioritize Developer C due to their relevant LMS experience, despite other developers potentially having more general web development experience. Traditional tag systems would struggle to make such nuanced distinctions.

### Additional Features in the System
1. **Third-Party Login:** We offer Google Firebase authentication for user convenience and security.
2. **Secure Communication:** Users can send communication requests with personal introductions, keeping details private until mutual acceptance. This includes email access for direct communication.
3. **Proactive Recommendations:** The system provides proactive recommendations based on user bios and project descriptions, connecting users with relevant opportunities automatically.

### Technical Documentation
- **Frontend:** Developed using React.
- **Backend:** Powered by Django.
- **Vector Database:** Utilizes Quadrant for storing vector embeddings.
- **Relational Database:** Utilizes SQLite for relational data storage.
- **Text to Vector Conversion:** Incorporates BERT models for converting text into vectors.

Our system aims to revolutionize open science project collaboration by enhancing discoverability and matching, while also ensuring security and ease of use for all users.

#### Tagging System Integration
Additionally, our system incorporates a tagging system. During the project's development, we initially explored the possibility of enhancing the traditional tag-based approach. This was done as a contingency plan while participating in a competition, as we were uncertain whether we could successfully implement the semantic search. However, as the project progressed, it became evident that the semantic search system was functioning exceptionally well, making the tagging system an auxiliary feature.

### Screenshots : 

