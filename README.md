# stockInformation

In this project, we access the financial performance of a listed company via its code.

## create environment:
    
For windows system open the Anaconda prompt:

    conda create my_env --name  python=3.9 -y
    conda run -n my_env pip install -r requirements.txt

## Execution:
    
### Data collection
    
    python -m src.api.access_stock_performance