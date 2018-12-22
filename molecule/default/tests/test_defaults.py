import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('distro, package', [
    ('centos,debian,ubuntu', 'iptables'),
    ('debian,ubuntu', 'iptables-persistent'),
])
def test_packages_is_installed(host, distro, package):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    assert host.package(package).is_installed


@pytest.mark.parametrize('distro, file', [
    ('centos', '/etc/sysconfig/iptables'),
    ('centos', '/etc/sysconfig/ip6tables'),
    ('debian,ubuntu', '/etc/iptables/rules.v4'),
    ('debian,ubuntu', '/etc/iptables/rules.v6'),
])
def test_configuration_file_exists(host, distro, file):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    file = host.file(file)
    assert file.exists


@pytest.mark.parametrize('distro, file', [
    ('centos', '/etc/sysconfig/iptables'),
    ('debian,ubuntu', '/etc/iptables/rules.v4'),

])
def test_syntax_iptables_v4(host, distro, file):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    cmd = 'iptables-restore --test < ' + file
    result = host.run(cmd)
    assert result.rc == 0


@pytest.mark.parametrize('distro, file', [
    ('centos', '/etc/sysconfig/ip6tables'),
    ('debian,ubuntu', '/etc/iptables/rules.v6'),
])
def test_syntax_iptables_v6(host, distro, file):
    if host.system_info.distribution not in distro:
        pytest.skip("skipping unmatch distribution")
    cmd = 'ip6tables-restore --test < ' + file
    result = host.run(cmd)
    assert result.rc == 0
