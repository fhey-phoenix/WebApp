require('dotenv').config()    
const express = require('express')    
const { OpenAIClient, AzureKeyCredential } = require("@azure/openai")    
const cors = require('cors')    
const apiKey = process.env.AZURE_OPENAI_API_KEY    
const endpoint = process.env.ENDPOINT  
    
const app = express()  
app.use(cors())    
app.use(express.json())    
    
app.post('/generate-answer', async (req, res) => {    
    const userquestion = req.body.userquestion    
    
    try {    
        const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey))    
        const deploymentId = "gpt-4-32k-deployment"    
        const events = await client.streamChatCompletions(    
            deploymentId,    
            [    
                { role: "system", content: "You are a helpful assistant." },    
                { role: "user", content: userquestion },    
            ],    
            { maxTokens: 1000 }    
        )
    
        res.setHeader('Content-Type', 'application/json');  
        for await (const event of events) {
            // console.log(event);
            for (const choice of event.choices) {  
                if (choice.delta?.content) {
                    // send the chunks of the response to the client in a streaming fashion  
                    res.write(choice.delta?.content);
                }  
            }    
        }  
        res.end();
    
    } catch (error) {    
        console.error(error)    
        res.status(500).send({ error: error.toString() })    
    }    
})    
    
app.listen(3000, () => console.log('Server listening on port 3000!'))    
