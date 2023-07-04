En CryptoReport podrás ingresar tus transacciones realizadas en este apasionante, a la par que frustrante, deprimente y conductor a la locura, mundo del trading de criptomonedas.

Introduciendo datos como la fecha y hora de la transacción, y las monedas que se ven involucradas (compra, venta y comisión), podrás tener un reporte exhaustivo de cuál ha sido tu rendimiento a lo largo de los años.


FUNCIONAMIENTO TÉCNICO:

Al registrar tu usuario te pediremos una API Key de CoinAPI, la cual puedes solicitar gratuitamente en https://www.coinapi.io/market-data-api/pricing, y mediante la cual iremos actualizando el valor de tus transacciones, con un tope de 100 al día, el límite que permite la API Key gratuita.

Registrando una transacción mediante formulario, o mediante un archivo .csv con un formato determinado, añadiremos una transacción a la base de datos, y las monedas y exchange correspondiente, en caso de no tenerlo ya registrado. Esta transacción tendrá un valor en USD de 0 por el momento.

Al activar las llamadas a CoinAPI se llenarán los campos que indican el valor de la moneda que hemos usado en la venta, así como el de la moneda usada para pagar la comisión, si es distinta; con esto tendremos el valor en dólares de la transacción, dato que necesitaremos para ir realizando los reportes.

Adicionalmente, se creará una "RawTransaction", donde "trocearemos" la transacción en 3 partes, una para la moneda comprada, otra para la moneda vendida, y otra para la moneda usada para pagar la comisión. Este procedimiento es usado para generar unos reportes aún más exhaustivos, y tener claridad al decimal de lo que hemos pagado en cada momento.

Estos reportes se mostrarán mediante gráficos de barras, torta, líneas etcétera, indicando comisiones pagadas a lo largo del tiempo, nuestro rendimiento durante un periodo determinado, aquellas monedas que nos han permitido ganar, las que nos han hecho perder, y mucho más.



¡Te damos la bienvenida!