#
# Conditional build:
%bcond_with	tests	# unit tests (require git checkout, not archive?)
%bcond_without	doc	# Sphinx documentation

Summary:	Python Git Library
Summary(pl.UTF-8):	Biblioteka Git dla Pythona
Name:		python3-git
Version:	3.1.44
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://github.com/gitpython-developers/GitPython/tags
Source0:	https://github.com/gitpython-developers/GitPython/archive/%{version}/GitPython-%{version}.tar.gz
# Source0-md5:	7e79b2d3a6e64ea5ef5a122c79723b39
URL:		https://pypi.org/project/GitPython/
# python 3.7 requires additionally mock
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ddt >= 1.1.1
BuildRequires:	python3-gitdb >= 4.0.1
BuildRequires:	python3-gitdb < 5
BuildRequires:	python3-pytest >= 7.3.1
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-instafail
BuildRequires:	python3-pytest-mock
BuildRequires:	python3-pytest-sugar
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-typing_extensions
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-gitdb >= 4.0.1
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 7.1.2
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GitPython is a Python library used to interact with git repositories,
high-level like git-porcelain, or low-level like git-plumbing.

It provides abstractions of git objects for easy access of repository
data, and additionally allows you to access the git repository more
directly using either a pure Python implementation, or the faster, but
more resource intensive git command implementation.

%description -l pl.UTF-8
GitPython to biblioteka Pythona służąca do pracy z repozytoriami gita,
wysokopoziomowo, jak git-porcelain lub niskopoziomowo, jak
git-plumbing.

Biblioteka udostępnia abstrakcje obiektów gita, zapewniając łatwy
dostęp do danych repozytorium, a ponadto pozwala na dostęp do
repozytorium bardziej bezpośrednio albo przy użyciu czysto pythonowej
implementacji, albo szybciej, ale z większym zużyciem zasobów, przy
użyciu implementacji poleceń gita.

%package apidocs
Summary:	API documentation for GitPython library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GitPython
Group:		Documentation

%description apidocs
API documentation for GitPython library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GitPython.

%prep
%setup -q -n GitPython-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_instafail,pytest_mock.plugin,pytest_sugar \
%{__python3} -m pytest test
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE README.md SECURITY.md
%dir %{py3_sitescriptdir}/git
%{py3_sitescriptdir}/git/*.py
%{py3_sitescriptdir}/git/index
%{py3_sitescriptdir}/git/objects
%{py3_sitescriptdir}/git/py.typed
%{py3_sitescriptdir}/git/refs
%{py3_sitescriptdir}/git/repo
%{py3_sitescriptdir}/git/__pycache__
%{py3_sitescriptdir}/GitPython-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,*.html,*.js}
%endif
