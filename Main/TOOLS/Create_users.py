import Tools as T
import random as rd

if __name__ == '__main__':
    bd = T.Crud_DB()

    print("*"*30)
    print("Registro de usuarios Temporal")
    print("*"*30)

    user = input("Usuario: ")
    password = input("Contraseña: ")

    workers = ["ADMINISTRADOR", "VENDEDOR", "CAJERO"]

    for ind, word in enumerate(workers):
        print(f"{ind+1}) {word}")

    worker = workers[int(input("Escoge el cargo: ")) - 1 ]
    print(worker)

    #Hasheando la contraseña
    hash = T.SimpleTools()


    hash_pas = hash.hashPassword(password)
    print("---->", len(hash_pas))

    #Generando cod_empleado
    cod_empleado = worker[0] + str(rd.randint(101,999) ) + "T"
    print(cod_empleado)

    # Insercion de datos
    try:
        query ="INSERT INTO Empleado_Datos(CodEmpleado, Usuario, Contrasena, Cargo) VALUES(?,?,?,?);"

        bd.getCursor().execute(query, cod_empleado, user, hash_pas, 'A')

        #query = "SELECT * FROM Empleado_Datos WHERE Contrasena = ?"
        #datos = bd.getCursor().execute(query, hash_pas)
        #print(datos.fetchall())

        bd.getCursor().commit()
        bd.getCursor().close()



        print("Datos Guradados correctamente")

    except  Exception as e:
        print(e)
        print(f"Error: -> {e.__str__()}")
