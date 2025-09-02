# Agentomics Extension

# Project Goal  
Extend the Agentomics framework to simulate how household, firm, and policy decisions aggregate into macroeconomic outcomes under shocks.  

# Key Features  
- Agents: Households, Firms, Government/Regulator, Central Bank, Financial & Global Markets, Social Network.  
- Decision-making: Mix of heuristic rules and LLM-driven agents (via Ollama).  
- Markets: Functional job and housing markets with supply, demand, and price dynamics.  
- Shocks: Interest rate changes, unemployment shocks, and stimulus programs.  

# Methods & Data  
- Integrated FRED data (UNRATE, CPIAUCSL) for validation.  
- Scenario runner to test policy and shock responses.  
- Logging + visualization of unemployment, wages, housing prices, and inequality.  

# Outputs  
- Reports: report.txt + scenario-specific summaries.  
- Plots: Unemployment, wages, housing prices, Gini coefficient.  
