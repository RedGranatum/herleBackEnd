from django.conf.urls import patterns, url
from clientes_pagos import views

urlpatterns =[
   url(r'^clientes_pagos/$', views.ClientesPagoLista.as_view(),name="clientes_pago_lista"),
   url(r'^clientes_pagos/detalles/(?P<venta>[0-9]+)/$', views.DetalleCargoAbonoPorVenta.as_view(),name="clientes_pagos_detalle_venta"),
   url(r'^clientes_pagos/agrupados/(?P<venta>[0-9]+)/$', views.SaldoAgrupadoPorVenta.as_view(),name="clientes_pagos_agrupado_venta"),
   url(r'^clientes_pagos/agrupados/adeudos/$', views.SaldoAgrupadoPorVentasConAdeudo.as_view(),name="clientes_pagos_agrupado_general_con_adeudo"),
   url(r'^calendario_pagos/$', views.ReporteCalendarioPagos.as_view(),name="clientes_pagos_calendario"),
   url(r'^calendario_acumulado_pagos/$', views.ReporteAcumuladoCalendarioPagos.as_view(),name="clientes_acumulado_pagos_calendario"),
   
]		

