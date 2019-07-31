
%define vendor_name Microsemi
%define vendor_label microsemi
%define driver_name aacraid

%define uname  4.19.0+1
%define module_dir updates


Summary: Driver for %{vendor_name} %{driver_name}
Name: microsemi-aacraid
Version: 1.2.1_52011
Release:56008                      
License: GPL
Source: %{name}-%{version}.tar.gz

BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} Linux Device Driver source.

%prep
%setup -q -n %{name}-%{version}

%build
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{uname}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{uname} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
%defattr(-,root,root,-)
/lib/modules/%{uname}/*/*.ko
%doc

%changelog
