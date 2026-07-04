"""
Tests for the Duérmete Niño application.
Covers models, views, API endpoints, and fixture data.
"""
from django.test import TestCase
from django.urls import reverse
import json

from .models import Arquetipo, Pais, SerFolclorico


# ============================================================
# MODEL TESTS
# ============================================================

class ArquetipoModelTest(TestCase):
    """Tests for the Arquetipo model."""

    def setUp(self):
        self.arquetipo = Arquetipo.objects.create(
            nombre="Test Arquetipo",
            descripcion="Una descripción de prueba para el arquetipo."
        )

    def test_arquetipo_creation(self):
        """Arquetipo can be created and counted."""
        self.assertEqual(Arquetipo.objects.count(), 1)

    def test_arquetipo_str_returns_nombre(self):
        """__str__ returns the nombre field."""
        self.assertEqual(str(self.arquetipo), "Test Arquetipo")

    def test_arquetipo_unique_nombre(self):
        """Duplicate nombre raises an integrity error."""
        with self.assertRaises(Exception):
            Arquetipo.objects.create(
                nombre="Test Arquetipo",
                descripcion="Duplicado"
            )

    def test_arquetipo_descripcion_corta_truncated(self):
        """descripcion_corta truncates long descriptions."""
        larga = "X" * 200
        arch = Arquetipo.objects.create(nombre="Largo", descripcion=larga)
        self.assertEqual(len(arch.descripcion_corta()), 83)  # 80 chars + '...'

    def test_arquetipo_descripcion_corta_short(self):
        """descripcion_corta returns full text when under 80 chars."""
        corta = "Corta desc"
        arch = Arquetipo.objects.create(nombre="Corto", descripcion=corta)
        self.assertEqual(arch.descripcion_corta(), corta)

    def test_arquetipo_ordering(self):
        """Arquetipos are ordered by nombre."""
        Arquetipo.objects.create(nombre="Beta", descripcion="")
        Arquetipo.objects.create(nombre="Alfa", descripcion="")
        names = list(Arquetipo.objects.values_list('nombre', flat=True))
        self.assertEqual(names, sorted(names))


class PaisModelTest(TestCase):
    """Tests for the Pais model."""

    def setUp(self):
        self.pais = Pais.objects.create(
            nombre="Testlandia",
            codigo_iso="TT",
            continente=Pais.Continentes.EUROPA
        )

    def test_pais_creation(self):
        """Pais can be created and counted."""
        self.assertEqual(Pais.objects.count(), 1)

    def test_pais_str_returns_nombre_and_code(self):
        """__str__ returns 'Nombre (ISO)'."""
        self.assertEqual(str(self.pais), "Testlandia (TT)")

    def test_pais_unique_codigo_iso(self):
        """Duplicate codigo_iso raises an integrity error."""
        with self.assertRaises(Exception):
            Pais.objects.create(
                nombre="Otra",
                codigo_iso="TT",
                continente=Pais.Continentes.ASIA
            )

    def test_pais_continente_choices_all_present(self):
        """All six continent choices are defined."""
        choices = dict(Pais.Continentes.choices)
        self.assertIn('EU', choices)
        self.assertIn('AS', choices)
        self.assertIn('AF', choices)
        self.assertIn('NA', choices)
        self.assertIn('SA', choices)
        self.assertIn('OC', choices)

    def test_pais_continente_display(self):
        """get_continente_display returns human-readable name."""
        self.assertEqual(self.pais.get_continente_display(), "Europa")
        self.pais.continente = Pais.Continentes.ASIA
        self.assertEqual(self.pais.get_continente_display(), "Asia")

    def test_pais_codigo_iso_max_length(self):
        """codigo_iso field has max_length=3."""
        field = Pais._meta.get_field('codigo_iso')
        self.assertEqual(field.max_length, 3)

    def test_pais_nombre_max_length(self):
        """nombre field has max_length=100."""
        field = Pais._meta.get_field('nombre')
        self.assertEqual(field.max_length, 100)

    def test_pais_ordering(self):
        """Paises are ordered by nombre."""
        Pais.objects.create(nombre="Zambia", codigo_iso="ZM", continente=Pais.Continentes.AFRICA)
        Pais.objects.create(nombre="Canada", codigo_iso="CA", continente=Pais.Continentes.NORTEAMERICA)
        names = list(Pais.objects.values_list('nombre', flat=True))
        self.assertEqual(names, sorted(names))


class SerFolcloricoModelTest(TestCase):
    """Tests for the SerFolclorico model."""

    def setUp(self):
        self.arquetipo = Arquetipo.objects.create(
            nombre="Protector",
            descripcion="Protege a los niños"
        )
        self.pais = Pais.objects.create(
            nombre="Testlandia",
            codigo_iso="TT",
            continente=Pais.Continentes.EUROPA
        )
        self.ser = SerFolclorico.objects.create(
            nombre="Test Creature",
            descripcion_breve="Una criatura de prueba",
            descripcion_detallada="Descripción detallada de prueba",
            pais=self.pais,
            arquetipo=self.arquetipo
        )

    def test_ser_creation(self):
        """SerFolclorico can be created and counted."""
        self.assertEqual(SerFolclorico.objects.count(), 1)

    def test_ser_str_returns_nombre_and_pais(self):
        """__str__ returns 'Nombre (País)'."""
        self.assertEqual(str(self.ser), "Test Creature (Testlandia)")

    def test_ser_pais_relation(self):
        """Ser is correctly linked to its Pais."""
        self.assertEqual(self.ser.pais, self.pais)

    def test_ser_arquetipo_relation(self):
        """Ser is correctly linked to its Arquetipo."""
        self.assertEqual(self.ser.arquetipo, self.arquetipo)

    def test_ser_arquetipo_nullable(self):
        """Arquetipo can be null on a SerFolclorico."""
        ser2 = SerFolclorico.objects.create(
            nombre="Orphan Creature",
            descripcion_breve="Sin arquetipo",
            pais=self.pais
        )
        self.assertIsNone(ser2.arquetipo)

    def test_ser_descripcion_breve_max_length(self):
        """descripcion_breve field has max_length=300."""
        field = SerFolclorico._meta.get_field('descripcion_breve')
        self.assertEqual(field.max_length, 300)

    def test_ser_nombre_max_length(self):
        """nombre field has max_length=200."""
        field = SerFolclorico._meta.get_field('nombre')
        self.assertEqual(field.max_length, 200)

    def test_ser_foreign_key_cascade(self):
        """Deleting a Pais cascades to its Seres."""
        pais_id = self.pais.id
        self.pais.delete()
        self.assertEqual(SerFolclorico.objects.filter(pais_id=pais_id).count(), 0)

    def test_ser_arquetipo_set_null_on_delete(self):
        """Deleting an Arquetipo sets arquetipo to null on its Seres."""
        arch_id = self.arquetipo.id
        self.arquetipo.delete()
        self.ser.refresh_from_db()
        self.assertIsNone(self.ser.arquetipo)

    def test_ser_reverse_relations(self):
        """Pais and Arquetipo have reverse relations to Seres."""
        self.assertIn(self.ser, self.pais.seres.all())
        self.assertIn(self.ser, self.arquetipo.seres.all())

    def test_ser_ordering(self):
        """Seres are ordered by pais__nombre, then nombre."""
        pais2 = Pais.objects.create(
            nombre="Aalandia",
            codigo_iso="AA",
            continente=Pais.Continentes.ASIA
        )
        ser_a = SerFolclorico.objects.create(
            nombre="Zeta Being", descripcion_breve="Z",
            pais=self.pais
        )
        ser_b = SerFolclorico.objects.create(
            nombre="Alpha Being", descripcion_breve="A",
            pais=pais2
        )
        names = list(SerFolclorico.objects.values_list('nombre', flat=True))
        # pais2 name "Aalandia" < self.pais name "Testlandia", so ser_b should come first
        self.assertEqual(names[0], ser_b.nombre)


# ============================================================
# VIEW TESTS (HTTP)
# ============================================================

class ViewTests(TestCase):
    """Tests for the HTML page views using Django's test client."""

    def test_home_view_status(self):
        """home_view returns 200 OK."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """home_view uses the home.html template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'duermete_nino/home.html')

    def test_home_view_context_has_titulo(self):
        """home_view context includes 'titulo' with 'Duérmete Niño'."""
        response = self.client.get(reverse('home'))
        self.assertIn('titulo', response.context)
        self.assertIn('Mitos y Leyendas Mundiales', response.context['titulo'])

    def test_arquetipos_view_status(self):
        """arquetipos_lista_view returns 200 OK."""
        response = self.client.get(reverse('arquetipos_lista'))
        self.assertEqual(response.status_code, 200)

    def test_arquetipos_view_uses_correct_template(self):
        """arquetipos_lista_view uses the arquetipos.html template."""
        response = self.client.get(reverse('arquetipos_lista'))
        self.assertTemplateUsed(response, 'duermete_nino/arquetipos.html')

    def test_arquetipos_view_context_has_arquetipos(self):
        """arquetipos_lista_view context includes 'arquetipos' queryset."""
        Arquetipo.objects.create(nombre="Test Arch", descripcion="Test")
        response = self.client.get(reverse('arquetipos_lista'))
        self.assertIn('arquetipos', response.context)
        self.assertEqual(len(response.context['arquetipos']), 1)

    def test_acerca_de_view_status(self):
        """acerca_de_view returns 200 OK."""
        response = self.client.get(reverse('acerca_de'))
        self.assertEqual(response.status_code, 200)

    def test_acerca_de_view_uses_correct_template(self):
        """acerca_de_view uses the acerca_de.html template."""
        response = self.client.get(reverse('acerca_de'))
        self.assertTemplateUsed(response, 'duermete_nino/acerca_de.html')

    def test_all_view_urls_resolve(self):
        """All named URL patterns resolve correctly."""
        self.assertEqual(reverse('home'), '/')
        self.assertEqual(reverse('arquetipos_lista'), '/arquetipos/')
        self.assertEqual(reverse('acerca_de'), '/acerca-de/')


# ============================================================
# API ENDPOINT TESTS
# ============================================================

class APITests(TestCase):
    """Tests for the JSON API endpoints."""

    def setUp(self):
        """Create minimal test data for API tests."""
        self.arquetipo = Arquetipo.objects.create(
            nombre="Test Arch",
            descripcion="Test"
        )
        self.pais = Pais.objects.create(
            nombre="Testland",
            codigo_iso="TT",
            continente=Pais.Continentes.EUROPA
        )
        self.ser = SerFolclorico.objects.create(
            nombre="Test Being",
            descripcion_breve="A test being",
            descripcion_detallada="Detailed test description",
            pais=self.pais,
            arquetipo=self.arquetipo
        )

    def test_api_lista_seres_status(self):
        """api_lista_seres returns 200 OK."""
        response = self.client.get(reverse('api_lista_seres'))
        self.assertEqual(response.status_code, 200)

    def test_api_lista_seres_json_structure(self):
        """api_lista_seres returns JSON with 'seres' list."""
        response = self.client.get(reverse('api_lista_seres'))
        data = json.loads(response.content)
        self.assertIn('seres', data)
        self.assertIsInstance(data['seres'], list)
        self.assertGreaterEqual(len(data['seres']), 1)

    def test_api_lista_seres_being_fields(self):
        """Each ser in the list has the correct fields."""
        response = self.client.get(reverse('api_lista_seres'))
        data = json.loads(response.content)
        being = data['seres'][0]
        self.assertIn('id', being)
        self.assertIn('nombre', being)
        self.assertIn('pais', being)
        self.assertIn('codigo_iso', being)
        self.assertIn('continente', being)
        self.assertIn('arquetipo', being)
        self.assertIn('descripcion_breve', being)

    def test_api_lista_seres_arquetipo_desconocido(self):
        """Ser without arquetipo shows 'Desconocido'."""
        ser2 = SerFolclorico.objects.create(
            nombre="Orphan",
            descripcion_breve="No arch",
            pais=self.pais
        )
        response = self.client.get(reverse('api_lista_seres'))
        data = json.loads(response.content)
        orphan = next(s for s in data['seres'] if s['id'] == ser2.id)
        self.assertEqual(orphan['arquetipo'], "Desconocido")

    def test_api_seres_por_pais_valid_status(self):
        """api_seres_por_pais returns 200 for valid ISO code."""
        response = self.client.get(
            reverse('api_seres_por_pais', args=[self.pais.codigo_iso])
        )
        self.assertEqual(response.status_code, 200)

    def test_api_seres_por_pais_valid_structure(self):
        """api_seres_por_pais returns correct JSON structure."""
        response = self.client.get(
            reverse('api_seres_por_pais', args=[self.pais.codigo_iso])
        )
        data = json.loads(response.content)
        self.assertEqual(data['pais'], 'Testland')
        self.assertIn('continente', data)
        self.assertIn('seres', data)
        self.assertEqual(len(data['seres']), 1)
        self.assertEqual(data['seres'][0]['nombre'], 'Test Being')
        self.assertIn('descripcion_detallada', data['seres'][0])

    def test_api_seres_por_pais_invalid_returns_404(self):
        """api_seres_por_pais returns 404 for invalid ISO code."""
        response = self.client.get(
            reverse('api_seres_por_pais', args=['ZZ'])
        )
        self.assertEqual(response.status_code, 404)

    def test_api_seres_por_pais_case_insensitive(self):
        """ISO code lookup is case-insensitive."""
        response = self.client.get(
            reverse('api_seres_por_pais', args=['tt'])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['pais'], 'Testland')

    def test_api_detalle_ser_valid_status(self):
        """api_detalle_ser returns 200 for valid ID."""
        response = self.client.get(
            reverse('api_detalle_ser', args=[self.ser.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_api_detalle_ser_valid_structure(self):
        """api_detalle_ser returns full ser details."""
        response = self.client.get(
            reverse('api_detalle_ser', args=[self.ser.id])
        )
        data = json.loads(response.content)
        self.assertEqual(data['nombre'], 'Test Being')
        self.assertEqual(data['pais'], 'Testland')
        self.assertEqual(data['arquetipo'], 'Test Arch')
        self.assertEqual(data['descripcion_breve'], 'A test being')
        self.assertEqual(data['descripcion_detallada'], 'Detailed test description')
        self.assertIn('id', data)

    def test_api_detalle_ser_invalid_returns_404(self):
        """api_detalle_ser returns 404 for invalid ID."""
        response = self.client.get(
            reverse('api_detalle_ser', args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_api_detalle_ser_arquetipo_null(self):
        """api_detalle_ser returns arquetipo=None when null."""
        ser2 = SerFolclorico.objects.create(
            nombre="Null Arch",
            descripcion_breve="Test",
            pais=self.pais
        )
        response = self.client.get(
            reverse('api_detalle_ser', args=[ser2.id])
        )
        data = json.loads(response.content)
        self.assertIsNone(data['arquetipo'])

    def test_api_views_return_json_content_type(self):
        """All API endpoints return application/json content type."""
        endpoints = [
            reverse('api_lista_seres'),
            reverse('api_seres_por_pais', args=[self.pais.codigo_iso]),
            reverse('api_detalle_ser', args=[self.ser.id]),
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(response['Content-Type'], 'application/json')


# ============================================================
# FIXTURE DATA TESTS
# ============================================================

class FixtureDataTests(TestCase):
    """Tests that the initial fixture data was loaded correctly."""

    fixtures = ['folclore_inicial.json']

    def test_all_arquetipos_loaded(self):
        """Exactly 5 arquetipos are loaded from fixture."""
        self.assertEqual(Arquetipo.objects.count(), 5)

    def test_all_paises_loaded(self):
        """Exactly 47 countries are loaded from fixture."""
        self.assertEqual(Pais.objects.count(), 47)

    def test_all_seres_loaded(self):
        """Exactly 100 folkloric beings are loaded from fixture."""
        self.assertEqual(SerFolclorico.objects.count(), 100)

    def test_all_continentes_represented(self):
        """All 6 continents have at least one country in the fixture."""
        continentes = set(Pais.objects.values_list('continente', flat=True))
        expected = {
            Pais.Continentes.EUROPA,
            Pais.Continentes.ASIA,
            Pais.Continentes.AFRICA,
            Pais.Continentes.NORTEAMERICA,
            Pais.Continentes.SURAMERICA,
            Pais.Continentes.OCEANIA,
        }
        self.assertEqual(continentes, expected)

    def test_seres_have_pais(self):
        """Every folkloric being is linked to a country."""
        seres_sin_pais = SerFolclorico.objects.filter(pais__isnull=True).count()
        self.assertEqual(seres_sin_pais, 0)

    def test_arquetipo_distribution(self):
        """Each archetype should have at least one being assigned."""
        for arch in Arquetipo.objects.all():
            count = SerFolclorico.objects.filter(arquetipo=arch).count()
            self.assertGreater(
                count, 0,
                f"Arquetipo '{arch.nombre}' has no beings assigned"
            )

    def test_europe_has_most_seres(self):
        """Europe should have the most beings (20 or more)."""
        europe = Pais.Continentes.EUROPA
        count = SerFolclorico.objects.filter(pais__continente=europe).count()
        self.assertGreaterEqual(count, 20)

    def test_especific_being_gryla_exists(self):
        """Grýla (Icelandic folklore) exists in the fixture data."""
        self.assertTrue(
            SerFolclorico.objects.filter(nombre__icontains='Grýla').exists()
        )

    def test_especific_being_llorona_exists(self):
        """La Llorona exists in the fixture data."""
        self.assertTrue(
            SerFolclorico.objects.filter(nombre__icontains='Llorona').exists()
        )

    def test_especific_being_kappa_exists(self):
        """Kappa (Japanese folklore) exists in the fixture data."""
        self.assertTrue(
            SerFolclorico.objects.filter(nombre__icontains='Kappa').exists()
        )

    def test_arquetipo_5_el_protector_del_hogar(self):
        """Arquetipo 5 is 'El protector del hogar'."""
        arch = Arquetipo.objects.get(pk=5)
        self.assertEqual(arch.nombre, "El protector del hogar")

    def test_pais_iceland_present(self):
        """Iceland (IS) is present in the fixture."""
        self.assertTrue(Pais.objects.filter(codigo_iso='IS').exists())

    def test_pais_japan_present(self):
        """Japan (JP) is present in the fixture."""
        self.assertTrue(Pais.objects.filter(codigo_iso='JP').exists())

    def test_pais_mexico_present(self):
        """Mexico (MX) is present in the fixture."""
        self.assertTrue(Pais.objects.filter(codigo_iso='MX').exists())

    def test_seres_linked_to_correct_pais(self):
        """Seres are correctly linked to their respective countries via FK."""
        # Spot-check: first ser in fixture linked to Iceland (pk=1)
        first_ser = SerFolclorico.objects.get(pk=1)
        self.assertEqual(first_ser.pais.codigo_iso, 'IS')

    def test_seres_linked_to_correct_arquetipo(self):
        """Seres are correctly linked to their respective arquetipos."""
        # Spot-check some known linkages from the fixture:
        # La Llorona (pk=21) is linked to arquetipo pk=3 (El espíritu acuático)
        llorona = SerFolclorico.objects.get(pk=21)
        self.assertEqual(llorona.arquetipo.pk, 3)
        self.assertEqual(llorona.arquetipo.nombre, "El espíritu acuático que atrae niños")

        # Jersey Devil (pk=49) is linked to arquetipo pk=2 (El secuestrador / Castigador)
        devil = SerFolclorico.objects.get(pk=49)
        self.assertEqual(devil.arquetipo.pk, 2)
