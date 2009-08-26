#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define		orig_name	tp_smapi
%define		rel		1
Summary:	sysfs interface to access ThinkPad's SMAPI functionality
Summary(pl.UTF-8):	Interfejs sysfs do funkcjonalności SMAPI ThinkPadów
Name:		kernel%{_alt_kernel}-misc-tp_smapi
Version:	0.40
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/tpctl/%{orig_name}-%{version}.tgz
# Source0-md5:	f4eb8bb4d4413a5ae65aa7d77f4112c0
URL:		http://tpctl.sourceforge.net/
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.19}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRequires:	rpmbuild(macros) >= 1.348
Requires(post,postun):  /sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sysfs interface to access ThinkPad's SMAPI functionality.

This package contains Linux kernel module.

%description -l pl.UTF-8
Interfejs sysfs do funkcjonalności SMAPI ThinkPadów.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n tp_smapi-%{version}
cat > Makefile <<'EOF'
obj-m := thinkpad_ec.o tp_smapi.o hdaps.o
EOF

%build
%build_kernel_modules -m tp_smapi,thinkpad_ec,hdaps EXTRA_CFLAGS="-I$PWD/include"

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m tp_smapi,thinkpad_ec,hdaps -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-misc-tp_smapi
%defattr(644,root,root,755)
%doc CHANGES README
/lib/modules/%{_kernel_ver}/misc/*.ko*
