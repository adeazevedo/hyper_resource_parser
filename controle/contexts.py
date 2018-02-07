from hyper_resource.contexts import FeatureContext, FeatureCollectionContext
class BusinessModelContext(FeatureContext):
    pass
class BusinessModelCollectionContext(FeatureCollectionContext):
    pass

class GastoContext(FeatureContext):
     def attributes_contextualized_dict(self):

        dic_context =  {
            "valor": {
                "@id": "http://schema.org/Float",
                "@type": "http://schema.org/Float"
            },
            "tipo_gasto": {
                "@id": "http://schema.org/Integer",
                "@type": "@id",
            },
            "usuario": {
                "@id": "http://schema.org/Person",
                "@type": "@id",

            },
            "detalhe": {
                "@id": "http://schema.org/Text",
                "@type": "http://schema.org/Text"

            },
            "id": {
                "@id": "http://schema.org/Integer",
                "@type": "http://schema.org/Integer"

            },
            "data": {
                "@id": "http://schema.org/Date",
                "@type": "http://schema.org/Date"

            }
        },

        return dic_context

class GastoCollectionContext(FeatureCollectionContext):
    def attributes_contextualized_dict(self):

        dic_context =  {
            "valor": {
                "@id": "http://schema.org/Float",
                "@type": "http://schema.org/Float"
            },
            "tipo_gasto": {
                "@id": "http://schema.org/Integer",
                "@type": "@id",
            },
            "usuario": {
                "@id": "http://schema.org/Person",
                "@type": "@id",

            },
            "detalhe": {
                "@id": "http://schema.org/Text",
                "@type": "http://schema.org/Text"

            },
            "id": {
                "@id": "http://schema.org/Integer",
                "@type": "http://schema.org/Integer"

            },
            "data": {
                "@id": "http://schema.org/Date",
                "@type": "http://schema.org/Date"

            }
        },

        return dic_context


class TipoGastoContext(FeatureContext):
    pass
class TipoGastoCollectionContext(FeatureCollectionContext):
    pass

class UsuarioContext(FeatureContext):
    pass
class UsuarioCollectionContext(FeatureCollectionContext):
    pass

