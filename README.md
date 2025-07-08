### Basic Chatbot with langgraph(Graph API)

#### Components of langgraph
- Edge
- Node
- state (this part will store the variables that will be utilised in some of the edges and nodes)

Yt videos --> Blog

- workflow
1. Yt vides --> Transcript
2. Transcript --> title
3. Title,Transcript --> Content


workflow graph:

            start(input as YT url)
              |
              |  - Edge (genreating transcript from Youtube URl using langchains YTloader)
         
         Transcript generator (node)
           
              |
              |  - transcript as variable traversing through edge
        
        Title Generator (Generates title based on Transcript Provided)
           
              |
              | - Transript and title traversing through this edge
        
        Content Generator (Generates content based on Transcript and Title Provided)

above diagram is StateGraph

### Chatbot with the tool

___Start___
     |
     |
tool_calling_llm (Node) (LLM with binding tools)
     |
     |
|            |
|            |
|        Tools (tavily API (internet search))
|               (Custom tools)
|            |
  ___END___


## ReACT Agent Architecture

1. Action - whenever input comes to LLM, LLM will make a tool call
2. Observe - When output comes from Tool Node, LLM observe, whether it should make tool call or go to the end node
3. Reason - The LLM analyzes the current task, the history of previous actions and observations, and the overall goal.This is analogous to a human thinking through a problem before acting.


### Adding Memory to the Agent

Adding Memory -
To persist the agent’s state, we use LangGraph’s MemorySaver, a built-in checkpointer. This checkpointer stores states in memory and associates them with a thread_id.

### Streaming technique

Flow - 
    Node1 --> Node 2 -- > Node3

Stream -
        mode = update
        mode = value (Appends the previous conversation in the list )
astream - 
        version = "v2"(Gives detailed conversation output)

{"message"=["Hi"]} -->  {"message"=["My Name is"]} --> {"message"=["Rohit"]}


### Human in the Loop

we are going to interuppt the workflow to get human feedback. We will disable parallel tool calling to avoid repeating the same query. Also, to avoid tool invocation when we resume the workflow