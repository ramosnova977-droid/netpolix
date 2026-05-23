from app.config.db import get_connection

class Calificacion:
    
    @staticmethod
    def calificar(cliente_id, video_isan, valor):
        valores_validos = ['excelente', 'buena', 'regular', 'mala']
        if valor not in valores_validos:
            return {"error": "Calificación inválida"}
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO calificacion (cliente_id, video_isan, valor, fecha)
                VALUES (%s, %s, %s, CURRENT_DATE)
            """, (cliente_id, video_isan, valor))
            
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Calificación registrada"}
        
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def obtener_calificaciones(video_isan):
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT valor, COUNT(*) FROM calificacion
                WHERE video_isan = %s
                GROUP BY valor
            """, (video_isan,))
            
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            valores_ponderados = {'excelente': 4, 'buena': 3, 'regular': 2, 'mala': 1}
            conteo = {'excelente': 0, 'buena': 0, 'regular': 0, 'mala': 0}
            total_votos = 0
            total_puntos = 0
            
            for row in rows:
                valor, cantidad = row
                conteo[valor] = cantidad
                total_votos += cantidad
                total_puntos += valores_ponderados[valor] * cantidad
            
            promedio = round(total_puntos / total_votos, 2) if total_votos > 0 else 0
            
            if promedio >= 3.5:
                promedio_texto = 'Excelente'
            elif promedio >= 2.5:
                promedio_texto = 'Buena'
            elif promedio >= 1.5:
                promedio_texto = 'Regular'
            elif promedio > 0:
                promedio_texto = 'Mala'
            else:
                promedio_texto = 'Sin calificaciones'
            
            return {
                "conteo": conteo,
                "total_votos": total_votos,
                "promedio": promedio,
                "promedio_texto": promedio_texto
            }
        
        except Exception as e:
            return {"error": str(e)}