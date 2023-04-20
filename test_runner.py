import xml.etree.ElementTree as ET
import unittest
import xmlrunner
import os
from test_temperature import TestTemperatureAPI
from test_aggregation import TestAggregation
from test_humidity import TestHumidityAPI

if __name__ == '__main__':
    # Exécuter les tests et stocker les résultats dans un fichier temporaire
    with open('test-results-temp.xml', 'w') as output:
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestTemperatureAPI)
        xmlrunner.XMLTestRunner(output=output).run(test_suite)

    # Exécuter les tests et stocker les résultats dans un fichier temporaire
    with open('test-results-temp2.xml', 'w') as output:
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAggregation)
        xmlrunner.XMLTestRunner(output=output).run(test_suite)

    # Exécuter les tests et stocker les résultats dans un fichier temporaire
    with open('test-results-temp3.xml', 'w') as output:
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestHumidityAPI)
        xmlrunner.XMLTestRunner(output=output).run(test_suite)

    # Fusionner les fichiers de résultats
    root = None
    for filename in ('test-results-temp.xml', 'test-results-temp2.xml', 'test-results-temp3.xml'):
        with open(filename, 'rb') as f:
            xml_data = f.read()
            tree = ET.fromstring(xml_data)
            if root is None:
                root = tree
            else:
                for node in tree.findall('testcase'):
                    root.append(node)
    result = ET.ElementTree(root)

    # Enregistrer les résultats fusionnés dans un fichier XML
    with open('test-results.xml', 'wb') as output:
        result.write(output)

    # Afficher le nombre de tests réussis/échoués
    total_tests = root.get('tests')
    failed_tests = root.get('failures')
    print(f'Total tests: {total_tests}, failed tests: {failed_tests}')
