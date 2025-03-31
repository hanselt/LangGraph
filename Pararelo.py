import time
from langgraph.graph import StateGraph
from typing import Annotated

# Estado del flujo con annotations para combinar resultados
class ParallelState(dict):
    task_1_result: str #Annotated[str, lambda x, y: f"{x}, {y}"]  # Combina strings
    task_2_result: str #Annotated[str, lambda x, y: f"{x}, {y}"]
    task_3_time: Annotated[float, lambda x, y: x if x > y else y] 
    tiempo_final: int

# Crear grafo
workflow = StateGraph(ParallelState)

# Nodos (simulan trabajos con delays)
def start_node(state):
    print("✅ Inicio del proceso")
    return {"task_1_result": "a", "task_2_result": "b" , "task_3_time":0.0}

def parallel_task_1(state):
    start_time = time.time()
    print("🔄 Task 1 iniciada...")
    time.sleep(2)  # Simula trabajo pesado (2 segundos)
    end_time = time.time()
    print("✔️ Task 1 completada")
    return {"task_1_result": "Resultado-1",
            "task_3_time": end_time - start_time  # Tiempo real: ~2s
            }

def parallel_task_2(state):
    start_time = time.time()
    print("🔄 Task 2 iniciada...")
    time.sleep(3)  # Simula trabajo más largo (3 segundos)
    end_time = time.time()
    print("✔️ Task 2 completada")
    return {"task_2_result": "Resultado-2",
            "task_3_time": end_time - start_time  # Tiempo real: ~3s
            }

def join_results(state):
    # total_time = state.get("task_3_time", 0) + 1  # Simula tiempo de consolidación
    print(f"\n🔗 Uniendo resultados: {state['task_1_result']} y {state['task_2_result']}")    
    return {"task_3_time": -1}

# Construir grafo
workflow.add_node("start", start_node)
workflow.add_node("task_1", parallel_task_1)
workflow.add_node("task_2", parallel_task_2)
workflow.add_node("join", join_results)

# Conexiones paralelas
workflow.set_entry_point("start")
workflow.add_edge("start", "task_1")
workflow.add_edge("start", "task_2")
workflow.add_edge("task_1", "join")
workflow.add_edge("task_2", "join")
workflow.set_finish_point("join")

# Compilar y ejecutar
app = workflow.compile()
print("🚀 Ejecutando grafo en paralelo...")
result = app.invoke({})
print("\n📊 Resultado final:", result)