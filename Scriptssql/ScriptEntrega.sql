USE [master]
GO
/****** Object:  Database [FERRETERIA_TERAN]    Script Date: 22/12/2021 21:17:36 ******/
CREATE DATABASE [FERRETERIA_TERAN]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'FERRETERIA_TERAN', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\FERRETERIA_TERAN.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'FERRETERIA_TERAN_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\FERRETERIA_TERAN_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [FERRETERIA_TERAN] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [FERRETERIA_TERAN].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ARITHABORT OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET  ENABLE_BROKER 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET RECOVERY FULL 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET  MULTI_USER 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [FERRETERIA_TERAN] SET DB_CHAINING OFF 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [FERRETERIA_TERAN] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'FERRETERIA_TERAN', N'ON'
GO
ALTER DATABASE [FERRETERIA_TERAN] SET QUERY_STORE = OFF
GO
USE [FERRETERIA_TERAN]
GO
/****** Object:  UserDefinedFunction [dbo].[actualizarStock]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   FUNCTION [dbo].[actualizarStock](
@CodProducto VARCHAR(20))
RETURNS Varchar(50)
AS
	BEGIN
		DECLARE @StockActual INT =(SELECT Stock FROM Producto WHERE Codigo = @CodProducto)
		RETURN(CONCAT('Ahora la cantidad es: ',@StockActual))
		
	END
GO
/****** Object:  UserDefinedFunction [dbo].[getActualStock]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*
Pruebass
EXEC updateStock 2,'C80'
EXEC updateStock 10,'C80'
*/

CREATE   FUNCTION [dbo].[getActualStock](
@CodProducto VARCHAR(20))
RETURNS Varchar(50)
AS
	BEGIN
		DECLARE @StockActual INT =(SELECT Stock FROM Producto WHERE Codigo = @CodProducto)
		RETURN(CONCAT('Ahora la cantidad es: ',@StockActual))
		
	END
GO
/****** Object:  UserDefinedFunction [dbo].[getAcutalStock]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   FUNCTION [dbo].[getAcutalStock](
@CodProducto VARCHAR(20))
RETURNS Varchar(50)
AS
	BEGIN
		DECLARE @StockActual INT =(SELECT Stock FROM Producto WHERE Codigo = @CodProducto)
		RETURN(CONCAT('Ahora la cantidad es: ',@StockActual))
		
	END
GO
/****** Object:  UserDefinedFunction [dbo].[getStock]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   FUNCTION [dbo].[getStock](@CodProducto VARCHAR(20))
RETURNS INT
AS 

	BEGIN
		RETURN(SELECT Stock FROM Producto WHERE Codigo = @CodProducto)
	END
GO
/****** Object:  Table [dbo].[Cargos]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cargos](
	[IdCargo] [char](1) NOT NULL,
	[Nombre] [varchar](20) NOT NULL,
 CONSTRAINT [PK_Cargos] PRIMARY KEY CLUSTERED 
(
	[IdCargo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Categoria]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Categoria](
	[Id] [int] NOT NULL,
	[Nombre] [varchar](20) NOT NULL,
	[Descripcion] [text] NOT NULL,
 CONSTRAINT [PK_Categoria] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Cliente]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cliente](
	[Dni] [char](8) NOT NULL,
	[Nombre] [varchar](20) NULL,
	[Apell_Paterno] [varchar](20) NULL,
	[Apell_Materno] [varchar](20) NULL,
	[Direccion] [varchar](50) NULL,
	[Telefono] [char](9) NULL,
 CONSTRAINT [PK__Cliente__C030857481EE8552] PRIMARY KEY CLUSTERED 
(
	[Dni] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Detalles de Pedido]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Detalles de Pedido](
	[CodPedido] [char](13) NOT NULL,
	[CodProducto] [varchar](20) NOT NULL,
	[cantidad] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DetallesUsuarios]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DetallesUsuarios](
	[CodEmpleado] [char](5) NOT NULL,
	[Usuario] [varchar](10) NOT NULL,
	[Contrasena] [varchar](40) NOT NULL,
	[Cargo] [char](1) NOT NULL,
	[Estado] [char](1) NOT NULL,
 CONSTRAINT [PK_Empleado_Datos_1] PRIMARY KEY CLUSTERED 
(
	[Usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DocEmitidos]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DocEmitidos](
	[ID_DM] [int] NOT NULL,
	[Documento] [varchar](20) NOT NULL,
 CONSTRAINT [PK_DocEmitidos] PRIMARY KEY CLUSTERED 
(
	[ID_DM] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Empleado]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Empleado](
	[CodEmpleado] [char](5) NOT NULL,
	[Dni] [char](8) NOT NULL,
	[Nombre] [varchar](20) NULL,
	[Ap_Paterno] [varchar](20) NULL,
	[Ap_Materno] [varchar](20) NULL,
	[Direccion] [varchar](50) NULL,
	[Telefono] [char](9) NULL,
 CONSTRAINT [PK_Empleado_1] PRIMARY KEY CLUSTERED 
(
	[CodEmpleado] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Estados]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Estados](
	[ID_E] [int] NOT NULL,
	[Estado] [varchar](20) NOT NULL,
 CONSTRAINT [PK_Estados] PRIMARY KEY CLUSTERED 
(
	[ID_E] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Marcas]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Marcas](
	[IdMarca] [int] NOT NULL,
	[Marca] [varchar](30) NULL,
 CONSTRAINT [PK_Marcas] PRIMARY KEY CLUSTERED 
(
	[IdMarca] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MPagos]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MPagos](
	[ID_MP] [int] NOT NULL,
	[Metodo_pago] [varchar](20) NOT NULL,
 CONSTRAINT [PK_MPagos] PRIMARY KEY CLUSTERED 
(
	[ID_MP] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Pedido]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Pedido](
	[CodPedido] [char](13) NOT NULL,
	[Monto] [float] NOT NULL,
	[Metodo de Pago] [int] NOT NULL,
	[Comprobante] [int] NOT NULL,
	[Estado] [int] NOT NULL,
	[Cliente] [char](8) NOT NULL,
	[Empleado] [char](5) NOT NULL,
	[fecha] [char](20) NOT NULL,
 CONSTRAINT [PK_Pedido] PRIMARY KEY CLUSTERED 
(
	[CodPedido] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Producto]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Producto](
	[Codigo] [varchar](20) NOT NULL,
	[Nombre] [varchar](20) NOT NULL,
	[Marca] [int] NOT NULL,
	[Precio] [float] NOT NULL,
	[Descripcion] [text] NOT NULL,
	[Stock] [int] NOT NULL,
	[U/Medida] [int] NOT NULL,
	[Categoria] [int] NOT NULL,
	[Proveedor] [char](11) NOT NULL,
	[U/Pedido] [int] NOT NULL,
 CONSTRAINT [PK_Producto] PRIMARY KEY CLUSTERED 
(
	[Codigo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Proveedor]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Proveedor](
	[RUC] [char](11) NOT NULL,
	[Nombre] [varchar](30) NOT NULL,
	[NombreContacto] [varchar](30) NOT NULL,
	[CargoContacto] [varchar](30) NOT NULL,
	[Direccion] [varchar](100) NOT NULL,
	[Ciudad] [varchar](30) NOT NULL,
	[Departamento] [varchar](30) NOT NULL,
	[Pais] [varchar](30) NOT NULL,
	[Correo] [varchar](30) NULL,
	[Telefono] [char](9) NOT NULL,
 CONSTRAINT [PK_Proveedor_1] PRIMARY KEY CLUSTERED 
(
	[RUC] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[UnidadesMedida]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[UnidadesMedida](
	[CodUM] [int] NOT NULL,
	[Unid_Med] [varchar](30) NULL,
 CONSTRAINT [PK_UnidadesMedida] PRIMARY KEY CLUSTERED 
(
	[CodUM] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[Cargos] ([IdCargo], [Nombre]) VALUES (N'A', N'ADMINISTRADOR')
INSERT [dbo].[Cargos] ([IdCargo], [Nombre]) VALUES (N'C', N'CAJERO')
INSERT [dbo].[Cargos] ([IdCargo], [Nombre]) VALUES (N'T', N'TRANSPORTISTA ')
INSERT [dbo].[Cargos] ([IdCargo], [Nombre]) VALUES (N'V', N'VENDEDOR')
GO
INSERT [dbo].[Categoria] ([Id], [Nombre], [Descripcion]) VALUES (3498, N'Alicates', N'Herramientas Pequeñas')
INSERT [dbo].[Categoria] ([Id], [Nombre], [Descripcion]) VALUES (6030, N'Inalambrico', N'Maquinas')
INSERT [dbo].[Categoria] ([Id], [Nombre], [Descripcion]) VALUES (8056, N'Percutores', N'Maquinas Percutores pequeñas')
GO
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'15346958', N'Luis', N'Apolo', N'Muñoz', N'Av_Los Quiones_185_Sauces', N'968569658')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'23568741', N'Brayan', N'Paredes', N'Espinoza', N'Av_Jorge Basadre_325_Sauces', N'979699965')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'25684102', N'Jeremias', N'Díaz ', N'Gómez', N'Av_Los Pinos_387_San Isidro', N'947365096')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'25698547', N'Lucas', N'Salazar', N'Muñoz', N'Av_Cristobal Bordiú _9865_Sauces', N'964625484')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'32659857', N'Andres', N'Rodríguez', N'Espinoza ', N'Av_Roma_235_Sauces', N'905134139')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'69852031', N'Alonso', N'Gómez', N'Rodríguez', N'Av_Los Quiones_172_Sauces', N'905960259')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'72854728', N'Elisa', N'Rodriguez', N'Quintana', N'Av_Victor Malasquez_55_Panamericana', N'943511091')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'72903465', N'Hernesto', N'Chavez', N'Roldan', N'Jr_La Uniòn_2_Uniòn', N'984388064')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'73618327', N'Piero', N'Salazar', N'Chumbe', N'Av_Victor Malasquez_315_Lima', N'992637111')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'75209346', N'Brenda', N'Ramos', N'Montoya', N'Av_Miguel Grau_14_Ica', N'934812065')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'76529488', N'Josue', N'Ramirez', N'Quispe', N'Calle_Los cernicalos_33_Amazonas', N'916619722')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'85746983', N'Jose', N'Rodríguez ', N'Díaz ', N'Av_Los Angeles_185_San Isidro', N'944663348')
INSERT [dbo].[Cliente] ([Dni], [Nombre], [Apell_Paterno], [Apell_Materno], [Direccion], [Telefono]) VALUES (N'96203145', N'Juan', N'Reyes', N'Muñoz', N'Av_Los Quiones_s/n_Sauces', N'968569658')
GO
INSERT [dbo].[Detalles de Pedido] ([CodPedido], [CodProducto], [cantidad]) VALUES (N'PTR8643      ', N'C80', 4)
INSERT [dbo].[Detalles de Pedido] ([CodPedido], [CodProducto], [cantidad]) VALUES (N'PTR6836      ', N'C80', 4)
GO
INSERT [dbo].[DetallesUsuarios] ([CodEmpleado], [Usuario], [Contrasena], [Cargo], [Estado]) VALUES (N'AD759', N'admin', N'–žïnÊÓÂš:b’€æ†Ï?]Z†¯óÊ’:Ül’', N'A', N'A')
INSERT [dbo].[DetallesUsuarios] ([CodEmpleado], [Usuario], [Contrasena], [Cargo], [Estado]) VALUES (N'VE789', N'brayanV', N'r¤.Éççñzük`†£‰NµœËhÍÌ¸Ö{]ôï', N'V', N'A')
INSERT [dbo].[DetallesUsuarios] ([CodEmpleado], [Usuario], [Contrasena], [Cargo], [Estado]) VALUES (N'CA456', N'elisa256', N'–žïnÊÓÂš:b’€æ†Ï?]Z†¯óÊ’:Ül’', N'C', N'A')
INSERT [dbo].[DetallesUsuarios] ([CodEmpleado], [Usuario], [Contrasena], [Cargo], [Estado]) VALUES (N'CA356', N'gonzales45', N'CAMBIAR_CONTRASEÑA', N'C', N'A')
INSERT [dbo].[DetallesUsuarios] ([CodEmpleado], [Usuario], [Contrasena], [Cargo], [Estado]) VALUES (N'AD356', N'lucas', N'CAMBIAR_CONTRASEÑA', N'A', N'A')
INSERT [dbo].[DetallesUsuarios] ([CodEmpleado], [Usuario], [Contrasena], [Cargo], [Estado]) VALUES (N'VE356', N'luquita', N'CAMBIAR_CONTRASEÑA', N'V', N'A')
GO
INSERT [dbo].[DocEmitidos] ([ID_DM], [Documento]) VALUES (0, N'None')
INSERT [dbo].[DocEmitidos] ([ID_DM], [Documento]) VALUES (1, N'Boleta')
INSERT [dbo].[DocEmitidos] ([ID_DM], [Documento]) VALUES (2, N'Factura')
GO
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'AD356', N'75945689', N'Luis', N'Gonzales', N'Pachas', N'Av_Los Quiñonez_600_Villa Hermosa', N'968532647')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'AD759', N'75945306', N'Luis', N'Quintana', N'Muñoz', N'Av_Los choristar_124_Lambayeque', N'946582135')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'CA356', N'45632189', N'Paco', N'Jimenez', N'Saavedra', N'Av_Los Condores_85_Urrunaga', N'963258749')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'CA456', N'45612378', N'Elisa', N'Fernandez', N'Muñoz', N'Av_Los pallares_123_Lambayeque', N'954652139')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'CA789', N'78965452', N'jhonathan', N'alvites', N'fernandez', N'Av_bolognesi_412_lambayeque', N'789521463')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'TR759', N'75945685', N'wwww', N'wdaaw', N'awdawdawd', N'Av_wwdwdwx_ cxzcxzvcx_xcvxzvcxc', N'568945623')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'VE356', N'75963214', N'Andres', N'Tapia', N'Flores', N'Av_Los Gallinazos_132_Urrunaga', N'963258741')
INSERT [dbo].[Empleado] ([CodEmpleado], [Dni], [Nombre], [Ap_Paterno], [Ap_Materno], [Direccion], [Telefono]) VALUES (N'VE789', N'78925361', N'brayan', N'alvites', N'fernandez', N'Calle_bolognesi_450_lambayeque', N'789456231')
GO
INSERT [dbo].[Estados] ([ID_E], [Estado]) VALUES (1, N'Pagado')
INSERT [dbo].[Estados] ([ID_E], [Estado]) VALUES (2, N'Pendiente')
GO
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (36, N'Argos')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (1505, N'Caterpillar')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (2107, N'asdqweqwo')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (3460, N'Dwalt')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (4014, N'asd')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (4357, N'Caterpillar')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (4555, N'Peruanito')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (4594, N'elios')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (5531, N'Caterpillar')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (5821, N'asdqweqwo')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (5967, N'asdsad')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (6301, N'llolol')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (6827, N'Caterpillar')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (6844, N'55')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (7755, N'proc')
INSERT [dbo].[Marcas] ([IdMarca], [Marca]) VALUES (8807, N'dasd')
GO
INSERT [dbo].[MPagos] ([ID_MP], [Metodo_pago]) VALUES (0, N'None')
INSERT [dbo].[MPagos] ([ID_MP], [Metodo_pago]) VALUES (1, N'Efectivo')
INSERT [dbo].[MPagos] ([ID_MP], [Metodo_pago]) VALUES (2, N'Tarjeta')
GO
INSERT [dbo].[Pedido] ([CodPedido], [Monto], [Metodo de Pago], [Comprobante], [Estado], [Cliente], [Empleado], [fecha]) VALUES (N'PTR6836      ', 62.4, 0, 0, 2, N'72854728', N'AD759', N'20/12/2021 19:43:20 ')
INSERT [dbo].[Pedido] ([CodPedido], [Monto], [Metodo de Pago], [Comprobante], [Estado], [Cliente], [Empleado], [fecha]) VALUES (N'PTR8643      ', 62.4, 0, 0, 2, N'72854728', N'AD759', N'20/12/2021 18:10:40 ')
GO
INSERT [dbo].[Producto] ([Codigo], [Nombre], [Marca], [Precio], [Descripcion], [Stock], [U/Medida], [Categoria], [Proveedor], [U/Pedido]) VALUES (N'C80', N'Alicate Max', 4555, 15.6, N'Uso domestico', 36, 106, 3498, N'10235698740', 0)
INSERT [dbo].[Producto] ([Codigo], [Nombre], [Marca], [Precio], [Descripcion], [Stock], [U/Medida], [Categoria], [Proveedor], [U/Pedido]) VALUES (N'P80', N'Martillo Percutor', 3460, 6000, N'300 V', 5, 103, 3498, N'10235698740', 0)
INSERT [dbo].[Producto] ([Codigo], [Nombre], [Marca], [Precio], [Descripcion], [Stock], [U/Medida], [Categoria], [Proveedor], [U/Pedido]) VALUES (N'P85', N'Guantes', 4555, 1550, N'Uso domestico', 30, 106, 3498, N'56985632147', 0)
GO
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'10235698563', N'Aceros SAC', N'Alexander', N'Vendedor', N'Jr_Ancash_470_Miraflores', N'Miraflores', N'Lima', N'Perú', N'Aceros@gmaiil.com', N'956425134')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'10235698740', N'Huemera SAC', N'Cristian', N'Vendedor', N'Av_Los Pibes_152_Amazonas', N'Bagua Chica', N'Amazonas', N'Peru', N'huemera@gmail.com', N'946538754')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'20147896523', N'Angel SAC', N'Marcos Jimenez', N'Prevendedor', N'Av_Pasaje Gutierrez_106_Mosquey', N'(medic Center Roshey)', N'Cusco', N'Perú', N'Angel@gmaiil.com', N'956425134')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'20165932145', N'Lucas SAC', N'Jose Bolivar', N'Prevendedor', N'Av_Los Angeles_185_San Isidro', N'Puerto Maldonado', N'Madre de Dios', N'Perú', N'lucas@gmaiil.com', N'956425134')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'20316598566', N'Los norteños Luis', N'Alex', N'Prevendedor', N'Calle_TACNA_345_CHICLAYO', N'Chiclayo', N'Lambayeque', N'Perú', N'Los_norteños@gmaiil.com', N'956425134')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'20569874532', N'Huemera SAC', N'Alex', N'Vendedor', N'Av_BOLOGNESI_725_CHICLAYO', N'CHICLAYO', N'LAMBAYEQUE', N'Perú', N'huemera@gmaiil.com', N'956425134')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'56985632147', N'Los Arcas', N'Piero Salazar', N'Prevendedor', N'Av_Los Arcas_235_Amazonas', N'Bagua', N'Amazonas', N'Peru', N'dwaltsac@gmail.com', N'968598650')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'78925413657', N'sodic SA', N'Carlos', N'vendedor', N'Av_bolognesi_963_lambayeque', N'chiclayo', N'lambayeque', N'Pais', N'carlos455@gmail.com', N'741369568')
INSERT [dbo].[Proveedor] ([RUC], [Nombre], [NombreContacto], [CargoContacto], [Direccion], [Ciudad], [Departamento], [Pais], [Correo], [Telefono]) VALUES (N'78952146387', N'pacasmayo', N'juan carlos', N'vendedor', N'Jr_juan pablo_432_pimentel', N'chiclayo', N'pimentel', N'peru', N'carlosj@gmail.com', N'741568925')
GO
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (101, N'Kilogramo')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (102, N'Metro')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (103, N'Metro Cuadrado')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (104, N'Cubo')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (105, N'Balde')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (106, N'Unidad')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (107, N'Litro')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (108, N'Tonelada')
INSERT [dbo].[UnidadesMedida] ([CodUM], [Unid_Med]) VALUES (109, N'Bolsa')
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Empleado]    Script Date: 22/12/2021 21:17:37 ******/
CREATE NONCLUSTERED INDEX [IX_Empleado] ON [dbo].[Empleado]
(
	[Dni] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Detalles de Pedido]  WITH CHECK ADD  CONSTRAINT [FK_Pedido_tiene_CodPedido] FOREIGN KEY([CodPedido])
REFERENCES [dbo].[Pedido] ([CodPedido])
GO
ALTER TABLE [dbo].[Detalles de Pedido] CHECK CONSTRAINT [FK_Pedido_tiene_CodPedido]
GO
ALTER TABLE [dbo].[Detalles de Pedido]  WITH CHECK ADD  CONSTRAINT [FK_Pedido_tiene_productos] FOREIGN KEY([CodProducto])
REFERENCES [dbo].[Producto] ([Codigo])
GO
ALTER TABLE [dbo].[Detalles de Pedido] CHECK CONSTRAINT [FK_Pedido_tiene_productos]
GO
ALTER TABLE [dbo].[DetallesUsuarios]  WITH CHECK ADD  CONSTRAINT [FK_Empleado_Datos_Empleado] FOREIGN KEY([CodEmpleado])
REFERENCES [dbo].[Empleado] ([CodEmpleado])
GO
ALTER TABLE [dbo].[DetallesUsuarios] CHECK CONSTRAINT [FK_Empleado_Datos_Empleado]
GO
ALTER TABLE [dbo].[DetallesUsuarios]  WITH CHECK ADD  CONSTRAINT [FK_Empleado_Datoscar] FOREIGN KEY([Cargo])
REFERENCES [dbo].[Cargos] ([IdCargo])
GO
ALTER TABLE [dbo].[DetallesUsuarios] CHECK CONSTRAINT [FK_Empleado_Datoscar]
GO
ALTER TABLE [dbo].[Pedido]  WITH CHECK ADD  CONSTRAINT [FK_Cliente] FOREIGN KEY([Cliente])
REFERENCES [dbo].[Cliente] ([Dni])
GO
ALTER TABLE [dbo].[Pedido] CHECK CONSTRAINT [FK_Cliente]
GO
ALTER TABLE [dbo].[Pedido]  WITH CHECK ADD  CONSTRAINT [FK_Pedid_docEmitido] FOREIGN KEY([Comprobante])
REFERENCES [dbo].[DocEmitidos] ([ID_DM])
GO
ALTER TABLE [dbo].[Pedido] CHECK CONSTRAINT [FK_Pedid_docEmitido]
GO
ALTER TABLE [dbo].[Pedido]  WITH CHECK ADD  CONSTRAINT [FK_Pedido_Empleado] FOREIGN KEY([Empleado])
REFERENCES [dbo].[Empleado] ([CodEmpleado])
GO
ALTER TABLE [dbo].[Pedido] CHECK CONSTRAINT [FK_Pedido_Empleado]
GO
ALTER TABLE [dbo].[Pedido]  WITH CHECK ADD  CONSTRAINT [FK_Pedido_Estados] FOREIGN KEY([Estado])
REFERENCES [dbo].[Estados] ([ID_E])
GO
ALTER TABLE [dbo].[Pedido] CHECK CONSTRAINT [FK_Pedido_Estados]
GO
ALTER TABLE [dbo].[Pedido]  WITH CHECK ADD  CONSTRAINT [Metodo_pago] FOREIGN KEY([Metodo de Pago])
REFERENCES [dbo].[MPagos] ([ID_MP])
GO
ALTER TABLE [dbo].[Pedido] CHECK CONSTRAINT [Metodo_pago]
GO
ALTER TABLE [dbo].[Producto]  WITH CHECK ADD  CONSTRAINT [FK_Producto_Categoria] FOREIGN KEY([Categoria])
REFERENCES [dbo].[Categoria] ([Id])
GO
ALTER TABLE [dbo].[Producto] CHECK CONSTRAINT [FK_Producto_Categoria]
GO
ALTER TABLE [dbo].[Producto]  WITH CHECK ADD  CONSTRAINT [FK_Producto_Marcas] FOREIGN KEY([Marca])
REFERENCES [dbo].[Marcas] ([IdMarca])
GO
ALTER TABLE [dbo].[Producto] CHECK CONSTRAINT [FK_Producto_Marcas]
GO
ALTER TABLE [dbo].[Producto]  WITH CHECK ADD  CONSTRAINT [FK_Producto_Proveedor] FOREIGN KEY([Proveedor])
REFERENCES [dbo].[Proveedor] ([RUC])
GO
ALTER TABLE [dbo].[Producto] CHECK CONSTRAINT [FK_Producto_Proveedor]
GO
ALTER TABLE [dbo].[Producto]  WITH CHECK ADD  CONSTRAINT [FK_Producto_UM] FOREIGN KEY([U/Medida])
REFERENCES [dbo].[UnidadesMedida] ([CodUM])
GO
ALTER TABLE [dbo].[Producto] CHECK CONSTRAINT [FK_Producto_UM]
GO
/****** Object:  StoredProcedure [dbo].[getReport]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
----Procedimiento que dara un reporte de las ventas 
CREATE   PROCEDURE [dbo].[getReport] 
@date1 DATETIME,@date2 DATETIME
AS 

SELECT p.Nombre Producto, p.Descripcion Descripcion, p.Precio Precio
, dp.cantidad
FROM [Detalles de Pedido] dp 
INNER JOIN Producto p ON p.Codigo = dp.CodProducto
INNER JOIN Pedido pe ON pe.CodPedido = dp.CodPedido
WHERE pe.fecha BETWEEN CAST(@date1 AS char(20)) AND CAST(@date2 as char(20))
GO
/****** Object:  StoredProcedure [dbo].[updateStock]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[updateStock](@cantidadARestar int ,
@CodProducto VARCHAR(20))
AS 
DECLARE @CantidaActual INT = (SELECT STOCK FROM Producto WHERE Codigo = @CodProducto)
DECLARE @CantidadResultante INT 
SET @CantidadResultante = @CantidaActual - @cantidadARestar
UPDATE Producto SET Stock = @CantidadResultante WHERE Codigo = @CodProducto
SELECT CONCAT('Ahora la cantidad actual es ', dbo.getActualStock(@CodProducto))
GO
/****** Object:  StoredProcedure [dbo].[usp_getNameProveedor]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[usp_getNameProveedor]
AS ---Retorna los noombres de compañias
SELECT Nombre FROM Proveedor
GO
/****** Object:  StoredProcedure [dbo].[usp_todasCategorias]    Script Date: 22/12/2021 21:17:37 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[usp_todasCategorias]
AS -----Todas las categorias
SELECT * FROM Categoria
GO
USE [master]
GO
ALTER DATABASE [FERRETERIA_TERAN] SET  READ_WRITE 
GO
