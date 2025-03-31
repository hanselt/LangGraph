from langgraph.graph import StateGraph, END

class WorkflowState(dict):
    mensaje_base: str
    mensaje_1: str
    mensaje_2:str

workflow = StateGraph(WorkflowState)

def nodo_entrada(state: WorkflowState):
    return {"mensaje_base": "Procesando en paralelo!"}

def nodo_procesamiento_1(state: WorkflowState):    
    return {"mensaje_1": " Nodo Uno"}

def nodo_procesamiento_2(state: WorkflowState):    
    return {"mensaje_2": " Nodo 2"}

def nodo_salida(state: WorkflowState):
    print("Mensaje Final:", state["mensaje_base"] + "->" + state["mensaje_1"] +" & "+ state["mensaje_2"])
    return state

workflow.add_node("entrada", nodo_entrada)
workflow.add_node("procesamiento_1", nodo_procesamiento_1)
workflow.add_node("procesamiento_2", nodo_procesamiento_2)
workflow.add_node("salida", nodo_salida)

workflow.set_entry_point("entrada")
workflow.add_edge("entrada", "procesamiento_1")
workflow.add_edge("entrada", "procesamiento_2")
workflow.add_edge("procesamiento_1", "salida")
workflow.add_edge("procesamiento_2", "salida")
workflow.set_finish_point("salida")

app = workflow.compile()
result = app.invoke({"mensaje": ""})
print("\nResultado completo:", result)