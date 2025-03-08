import math
from fpdf import FPDF
import sympy as sp

# Función de punto fijo utilizando sympy
def punto_fijo(xi, g_func, f_func, expresion_mostrar_g, expresion_mostrar_f, error_max=0.0001, max_iter=100, decimales=6):
    iteraciones = []
    xi_mas_uno = xi
    error = float('inf')
    
    for i in range(max_iter):
        xi_anterior = xi_mas_uno
        try:
            xi_mas_uno = g_func(xi_anterior)
            if not math.isfinite(xi_mas_uno):
                print(f"Error: La función g(x) produjo un valor no finito en x = {xi_anterior}")
                return iteraciones, xi_anterior, None, None, None
        except Exception as e:
            print(f"Error al evaluar g({xi_anterior}): {e}")
            return iteraciones, xi_anterior, None, None, None
        
        if xi_mas_uno == 0:
            error = float('inf')
        else:
            error = abs((xi_mas_uno - xi_anterior) / xi_mas_uno)
        
        formula_valor = f"{xi_mas_uno:.{decimales}f}"
        
        # Evaluar f(x) en el valor xi_mas_uno
        valor_fx = f_func(xi_mas_uno)  # Evaluación de f(x) con el último xi
        formula_fx_iter = f"f(x) = {expresion_mostrar_f}"  # Fórmula de la función f(x)
        resultado_fx_iter = f"f({xi_mas_uno:.{decimales}f}) = {valor_fx:.{decimales}f}"  # Resultado de la evaluación
        
        iteraciones.append({
            'Iteración': i + 1,
            'xi': xi_anterior,
            'xi_mas_uno': xi_mas_uno,
            'Error': error,
            'Formula_xi+1': f"x_{i+1} = g({xi_anterior:.{decimales}f}) = {expresion_mostrar_g.replace('x', str(round(xi_anterior, decimales)))} = {formula_valor}",
            'Formula_Error': f"Error = |({xi_mas_uno:.{decimales}f} - {xi_anterior:.{decimales}f}) / {xi_mas_uno:.{decimales}f}| = {error:.{decimales}f}",
            'Formula_fx': f"  {formula_fx_iter.replace('x', str(round(xi_mas_uno, decimales)))} = {resultado_fx_iter}"
        })
        
        if error <= error_max:
            break
    
    # Evaluar f(x) con el último valor de xi_mas_uno
    valor_fx = f_func(xi_mas_uno)  # Evaluación de f(x) con el último xi
    formula_fx = f"f(x) = {expresion_mostrar_f}"  # Fórmula de la función f(x)
    resultado_fx = f"f({xi_mas_uno:.{decimales}f}) = {valor_fx:.{decimales}f}"  # Resultado de la evaluación

    return iteraciones, xi_mas_uno, valor_fx, formula_fx, resultado_fx

# Función para generar el PDF
def generar_pdf(nombre_estudiante, iteraciones, raiz, funcion_f, funcion_gx, evaluacion_final, decimales, formula_fx, resultado_fx):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f'Método de Punto Fijo - {nombre_estudiante}', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f'Función utilizada: {funcion_f}')
    pdf.multi_cell(0, 10, f'Función g(x): {funcion_gx}')
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 12)
    pdf.multi_cell(0, 10, 'Iteraciones realizadas:')
    pdf.ln(5)
    pdf.set_font('Arial', '', 10)
    
    for iteracion in iteraciones:
        pdf.multi_cell(0, 10, f"Iteración {iteracion['Iteración']}:")
        pdf.multi_cell(0, 10, f"  xi = {iteracion['xi']:.{decimales}f}")
        pdf.multi_cell(0, 10, f"  {iteracion['Formula_xi+1']}")
        pdf.multi_cell(0, 10, f"  {iteracion['Formula_Error']}")
        pdf.multi_cell(0, 10, f"  {iteracion['Formula_fx']}")
        pdf.ln(3)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(30, 10, 'Iteración', 1, 0, 'C')
    pdf.cell(40, 10, 'xi', 1, 0, 'C')
    pdf.cell(40, 10, 'xi+1', 1, 0, 'C')
    pdf.cell(40, 10, 'Error', 1, 1, 'C')
    pdf.set_font('Arial', '', 10)
    
    for iteracion in iteraciones:
        pdf.cell(30, 10, str(iteracion['Iteración']), 1, 0, 'C')
        pdf.cell(40, 10, f"{iteracion['xi']:.{decimales}f}", 1, 0, 'C')
        pdf.cell(40, 10, f"{iteracion['xi_mas_uno']:.{decimales}f}", 1, 0, 'C')
        pdf.cell(40, 10, f"{iteracion['Error']:.{decimales}f}", 1, 1, 'C')
    
    pdf.ln(10)
    
    # Incluir la evaluación de f(x) con el último valor de xi+1 debajo de la tabla
    pdf.set_font('Arial', 'I', 12)
    if evaluacion_final is not None:
        pdf.multi_cell(0, 10, f'Fórmula de f(x): {formula_fx}')
        pdf.multi_cell(0, 10, f'Valor de f(x) con x = {raiz:.{decimales}f}: {resultado_fx}')
    else:
        pdf.multi_cell(0, 10, 'No se pudo encontrar una raíz válida')

    # Guardar el PDF en la ruta especificada
    pdf.output(r"C:\Users\JP\Documents\Analisis_numerico_2025_1\Metodo_Punto_Fijo_Error.pdf")

# Convertir la expresión del usuario usando sympy
def convertir_a_funcion_sympy(expresion):
    """Convierte una expresión matemática a una función utilizando sympy"""
    x = sp.symbols('x')
    expresion = expresion.replace("^", "**")
    return sp.sympify(expresion)

# Solicitar la función f(x) al usuario de forma amigable
print("Ingrese la función f(x) para el método del punto fijo.")
print("Ejemplos: 2*x**2-x-5 o exp(x) o e**x")
expresion_usuario_f = input("f(x) = ")

# Solicitar la función g(x) al usuario de forma amigable
print("Ingrese la función g(x) para el método del punto fijo.")
expresion_usuario_g = input("g(x) = ")

# Convertir las expresiones del usuario a funciones sympy
f_expr = convertir_a_funcion_sympy(expresion_usuario_f)
g_expr = convertir_a_funcion_sympy(expresion_usuario_g)

# Crear funciones dinámicas a partir de las expresiones
def crear_funcion(f_expr):
    """Convierte una expresión simbólica de sympy a una función evaluable en números"""
    return sp.lambdify(sp.symbols('x'), f_expr, 'math')

# Crear las funciones f(x) y g(x) dinámicamente
f_func = crear_funcion(f_expr)
g_func = crear_funcion(g_expr)

# Ingresar valor inicial xi
xi = float(input("Ingrese el valor inicial xi: "))
decimales = int(input("Ingrese el número de decimales para los resultados: "))

# Usar la expresión original del usuario para mostrar en el PDF
iteraciones, raiz, evaluacion_final, formula_fx, resultado_fx = punto_fijo(xi, g_func, f_func, expresion_usuario_g, expresion_usuario_f, decimales=decimales)

# Generar el PDF y guardarlo en la ruta especificada
generar_pdf('Jhon Peinado & Mayra Toro', iteraciones, raiz, f"f(x) = {expresion_usuario_f}", f"g(x) = {expresion_usuario_g}", evaluacion_final, decimales, formula_fx, resultado_fx)

print("El PDF ha sido generado exitosamente.")
