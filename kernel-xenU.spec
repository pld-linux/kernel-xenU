#
# NOTE:
# the following bcond combos will not work
# - without_vserver and any of the following
#   - with_apparmor
#   - with_grsec_minimal
#   - with_grsec_full
#
# LATEST VERSION CHECKER:
# # curl -s http://www.kernel.org/kdist/finger_banner
#
# TODO:
# - benchmark NO_HZ & HZ=1000 vs HZ=300 on i686
# - update or remove tahoe9xx patch2
# - update grsec_minimal patch1000:
#   fs/proc/base.c:1484: error: 'struct task_struct' has no member named 'uid'
#
# HOWTO update configuration files:
# - run build
# - add new options to proper config (kernel-multiarch.config, kernel-x86.config, kernel-powerpc.config etc)
# - sort configuration files using:
#   ./kernel-config-sort.pl ~/rpm/BUILD/kernel-%{version}/linux-%{version}/ -a x86 kernel-x86.config
#   ./kernel-config-sort.pl ~/rpm/BUILD/kernel-%{version}/linux-%{version} kernel-multiarch.config
#
# Conditional build:
%bcond_without	source		# don't build kernel-source package
%bcond_without	doc			# don't build kernel-doc package
%bcond_without	pcmcia		# don't build pcmcia

%bcond_with	verbose		# verbose build (V=1)

%bcond_with	pae		# build PAE (HIGHMEM64G) support on uniprocessor
%bcond_with	nfsroot		# build with root on NFS support

%bcond_without	imq		# imq support
%bcond_without	esfq		# esfq support
%bcond_without	ipv6		# ipv6 support

%bcond_without	vserver		# support for VServer (enabled by default)

%bcond_with	myown		# build with your own config (kernel-myown.config)

%{?debug:%define with_verbose 1}

%define		have_drm	0
%define		have_oss	0
%define		have_sound	0
%define		have_pcmcia	0

%define		have_pcmcia	0

%define		basever		2.6.35
%define		postver		.4
%define		rel		0.1

%define		_enable_debug_packages			0

%define		tuxonice_version	3.1.1.1
%define		netfilter_snap		20070806

%define		_alt_kernel	xenU

%if %{with myown}
%if "%{_alt_kernel}" == "xenU"
%define		alt_kernel	myown
%endif
%endif

# kernel release (used in filesystem and eventually in uname -r)
# modules will be looked from /lib/modules/%{kernel_release}
# localversion is just that without version for "> localversion"
%define		localversion	%{rel}
%define		kernel_release	%{version}%{?alt_kernel:_%{alt_kernel}}-%{localversion}

Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de.UTF-8):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(et.UTF-8):	Linuxi kernel (ehk operatsioonisüsteemi tuum)
Summary(fr.UTF-8):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl.UTF-8):	Jądro Linuksa
Name:		kernel-%{_alt_kernel}
Version:	%{basever}%{postver}
Release:	%{rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{basever}.tar.bz2
# Source0-md5:	091abeb4684ce03d1d936851618687b6
%if "%{postver}" != "%{nil}"
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	738f762746488345b1a8707d00895eef
%endif

Source3:	kernel-xenU-autoconf.h
Source4:	kernel-xenU-config.h
Source6:	kernel-xenU-config.awk
Source7:	kernel-xenU-module-build.pl
Source8:	kernel-xenU-track-config-change.awk
# not used by kernel.spec, but it's good to have it in SOURCES
Source9:	kernel-xenU-config-sort.pl
Source10:	kernel-xenU.make

Source20:	kernel-xenU-multiarch.config
Source21:	kernel-xenU-x86.config

Source40:	kernel-xenU-netfilter.config
Source43:	kernel-xenU-vserver.config

Source50:	kernel-xenU-no-pax.config

Source59:	kernel-xenU-bzip2-lzma.config

# based on http://vserver.13thfloor.at/Experimental/patch-2.6.35-vs2.3.0.36.31.diff
Patch100:	kernel-xenU-vserver-2.3.patch
Patch101:	kernel-xenU-vserver-fixes.patch

URL:		http://www.kernel.org/
BuildRequires:	binutils >= 3:2.18
BuildRequires:	/sbin/depmod
BuildRequires:	gcc >= 5:3.2
BuildRequires:	xz >= 1:4.999.7
AutoReqProv:	no
# for hostname command
BuildRequires:	module-init-tools >= 3.5
BuildRequires:	net-tools
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.5-24
BuildRequires:	rpmbuild(macros) >= 1.217
Requires(post):	coreutils
Requires(post):	geninitrd >= 10000-3
Requires(post):	module-init-tools >= 0.9.9
Requires:	/sbin/depmod
Requires:	coreutils
Requires:	geninitrd >= 10000-3
Requires:	module-init-tools >= 0.9.9
Provides:	%{name}(netfilter) = %{netfilter_snap}
Provides:	%{name}(vermagic) = %{kernel_release}
Conflicts:	e2fsprogs < 1.29
Conflicts:	isdn4k-utils < 3.1pre1
Conflicts:	jfsutils < 1.1.3
Conflicts:	lvm2 < 2.02.40
Conflicts:	module-init-tools < 0.9.10
Conflicts:	nfs-utils < 1.0.5
Conflicts:	oprofile < 0.9
Conflicts:	ppp < 1:2.4.0
Conflicts:	procps < 3.2.0
Conflicts:	quota-tools < 3.09
Conflicts:	reiserfsprogs < 3.6.3
Conflicts:	rpm < 4.4.2-0.2
Conflicts:	udev < 1:081
Conflicts:	util-linux < 2.10o
Conflicts:	util-vserver < 0.30.216
Conflicts:	xfsprogs < 2.6.0
%if %{with pae}
ExclusiveArch:	pentium3 pentium4 athlon i686 %{x8664}
%else
ExclusiveArch:	%{ix86} %{x8664}
%endif
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target_arch_dir		x86

%define		defconfig	arch/%{target_arch_dir}/defconfig

# No ELF objects there to strip (skips processing 27k files)
%define		_noautostrip	\\(.*%{_kernelsrcdir}/.*\\|.*/vmlinux.*\\)
%define		_noautochrpath	.*%{_kernelsrcdir}/.*

%define		initrd_dir	/boot

%define		topdir		%{_builddir}/%{name}-%{version}
%define		srcdir		%{topdir}/linux-%{basever}
%define		objdir		%{topdir}/%{targetobj}
%define		targetobj	%{_target_base_arch}-gcc-%(%{kgcc} -dumpversion)

%define		_kernelsrcdir	/usr/src/linux%{_alt_kernel}-%{version}

%if "%{_target_base_arch}" != "%{_arch}"
	%define CrossOpts ARCH=%{_target_base_arch} CROSS_COMPILE=%{_target_cpu}-pld-linux-
	%define	DepMod /bin/true

	%if "%{_arch}" == "x86_64" && "%{_target_base_arch}" == "i386"
	%define	CrossOpts ARCH=%{_target_base_arch} CC="%{__cc}"
	%define	DepMod /sbin/depmod
	%endif

%else
	%define CrossOpts ARCH=%{_target_base_arch} CC="%{__cc}"
	%define	DepMod /sbin/depmod
%endif
%define MakeOpts %{CrossOpts} HOSTCC="%{__cc}"

%define __features Netfilter module dated: %{netfilter_snap}\
%{?with_nfsroot:Root on NFS - enabled}\
%{?with_vserver:VServer     - enabled}\

%define Features %(echo "%{__features}" | sed '/^$/d')

%description
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

%{Features}

%description -l de.UTF-8
Das Kernel-Paket enthält den Linux-Kernel (vmlinuz), den Kern des
Linux-Betriebssystems. Der Kernel ist für grundliegende
Systemfunktionen verantwortlich: Speicherreservierung,
Prozeß-Management, Geräte Ein- und Ausgaben, usw.

%{Features}

%description -l fr.UTF-8
Le package kernel contient le kernel linux (vmlinuz), la partie
centrale d'un système d'exploitation Linux. Le noyau traite les
fonctions basiques d'un système d'exploitation: allocation mémoire,
allocation de process, entrée/sortie de peripheriques, etc.

%{Features}

%description -l pl.UTF-8
Pakiet zawiera jądro Linuksa niezbędne do prawidłowego działania
Twojego komputera. Zawiera w sobie sterowniki do sprzętu znajdującego
się w komputerze, takiego jak sterowniki dysków itp.

%{Features}

%package vmlinux
Summary:	vmlinux - uncompressed kernel image
Summary(de.UTF-8):	vmlinux - dekompressiertes Kernel Bild
Summary(pl.UTF-8):	vmlinux - rozpakowany obraz jądra
Group:		Base/Kernel
Obsoletes:	kernel-smp-vmlinux

%description vmlinux
vmlinux - uncompressed kernel image.

%description vmlinux -l de.UTF-8
vmlinux - dekompressiertes Kernel Bild.

%description vmlinux -l pl.UTF-8
vmlinux - rozpakowany obraz jądra.

%package headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
Group:		Development/Building
Provides:	%{name}-headers(netfilter) = %{netfilter_snap}
AutoReqProv:	no

%description headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten, die beim rekompilieren des
Kernels oder bei Kernel Modul kompilationen gebraucht werden.

%description headers -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe jądra, niezbędne do rekompilacji jądra
oraz budowania modułów jądra.

%package module-build
Summary:	Development files for building kernel modules
Summary(de.UTF-8):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl.UTF-8):	Pliki służące do budowania modułów jądra
Group:		Development/Building
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Conflicts:	rpmbuild(macros) < 1.550
AutoReqProv:	no

%description module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description module-build -l de.UTF-8
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description module-build -l pl.UTF-8
Pliki ze drzewa źródeł jądra potrzebne do budowania modułów jądra
Linuksa z zewnętrznych pakietów.

%package source
Summary:	Kernel source tree
Summary(de.UTF-8):	Der Kernel Quelltext
Summary(pl.UTF-8):	Kod źródłowy jądra Linuksa
Group:		Development/Building
Requires:	%{name}-module-build = %{epoch}:%{version}-%{release}
AutoReqProv:	no

%description source
This is the source code for the Linux kernel. You can build a custom
kernel that is better tuned to your particular hardware.

%description source -l de.UTF-8
Das Kernel-Source-Paket enthält den source code (C/Assembler-Code) des
Linux-Kernels. Die Source-Dateien werden gebraucht, um viele
C-Programme zu kompilieren, da sie auf Konstanten zurückgreifen, die
im Kernel-Source definiert sind. Die Source-Dateien können auch
benutzt werden, um einen Kernel zu kompilieren, der besser auf Ihre
Hardware ausgerichtet ist.

%description source -l fr.UTF-8
Le package pour le kernel-source contient le code source pour le noyau
linux. Ces sources sont nécessaires pour compiler la plupart des
programmes C, car il dépend de constantes définies dans le code
source. Les sources peuvent être aussi utilisée pour compiler un noyau
personnalisé pour avoir de meilleures performances sur des matériels
particuliers.

%description source -l pl.UTF-8
Pakiet zawiera kod źródłowy jądra systemu.

%package doc
Summary:	Kernel documentation
Summary(de.UTF-8):	Kernel Dokumentation
Summary(pl.UTF-8):	Dokumentacja do jądra Linuksa
Group:		Documentation
AutoReqProv:	no

%description doc
This is the documentation for the Linux kernel, as found in
/usr/src/linux/Documentation directory.

%description doc -l de.UTF-8
Dies ist die Kernel Dokumentation wie sie im 'Documentation'
Verzeichniss vorgefunden werden kann.

%description doc -l pl.UTF-8
Pakiet zawiera dokumentację do jądra Linuksa pochodzącą z katalogu
/usr/src/linux/Documentation.

%prep
%setup -qc
ln -s %{SOURCE7} kernel-module-build.pl
ln -s %{SOURCE10} Makefile
cd linux-%{basever}

# hack against warning in pax/grsec
sed -i 's/-Werror//' arch/alpha/kernel/Makefile

%if "%{postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | patch -p1 -s
%endif

# vserver
%if %{with vserver}
%patch100 -p1
%patch101 -p1
%endif

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{postver}%{?alt_kernel:_%{alt_kernel}}#g' Makefile

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -f

%build
install -d %{objdir}
cat > %{targetobj}.mk <<'EOF'
# generated by %{name}.spec
KERNELSRC		:= %{_builddir}/%{name}-%{version}/linux-%{basever}
KERNELOUTPUT	:= %{objdir}

SRCARCH		:= %{target_arch_dir}
ARCH		:= %{_target_base_arch}
Q			:= %{!?with_verbose:@}
MAKE_OPTS	:= %{MakeOpts}
DEFCONFIG   := %{defconfig}
EOF

BuildConfig() {
	%{?debug:set -x}
	set -e

	Config="kernel-xenU-%{target_arch_dir}.config"
	echo >&2 "Building config file for %{_target_cpu} using $Config et al."

	# prepare local and important options
	cat <<-EOCONFIG > important.config
		LOCALVERSION="-%{localversion}"

%if 0%{?debug:1}
		CONFIG_DEBUG_SLAB=y
		CONFIG_DEBUG_SLAB_LEAK=y
		CONFIG_DEBUG_PREEMPT=y
		CONFIG_RT_DEADLOCK_DETECT=y
%endif

%if %{without ipv6}
		CONFIG_IPV6=n
%endif

%ifarch i686 athlon pentium3 pentium4
  %if %{with pae}
		CONFIG_HIGHMEM4G=n
		CONFIG_HIGHMEM64G=y
		CONFIG_X86_PAE=y
		CONFIG_NUMA=n
  %endif
%endif

%if %{with nfsroot}
		CONFIG_NFS_FS=y
		CONFIG_ROOT_NFS=y
%endif

EOCONFIG

	# prepare kernel-style config file from multiple config files
	%{__awk} -v arch="all %{target_arch_dir} %{_target_base_arch} %{_target_cpu}" -f %{SOURCE6} \
%if %{with myown}
		$RPM_SOURCE_DIR/kernel-xenU-%{alt_kernel}.config \
%endif
		important.config \
		\
%if %{with vserver}
		%{SOURCE43} \
%endif
		%{SOURCE40} %{?0:netfilter} \
		%{SOURCE20} \
		$RPM_SOURCE_DIR/$Config
}

cd %{objdir}
install -d arch/%{target_arch_dir}
BuildConfig > %{defconfig}
ln -sf %{defconfig} .config
cd -

%{__make} \
	TARGETOBJ=%{targetobj} \
	%{?with_verbose:V=1} \
	oldconfig

%{__awk} %{?debug:-v dieOnError=1} -v infile=%{objdir}/%{defconfig} -f %{SOURCE8} %{objdir}/.config

# build kernel
%{__make} \
	TARGETOBJ=%{targetobj} \
	%{?with_verbose:V=1} \
	all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} %{MakeOpts} %{!?with_verbose:-s} modules_install firmware_install \
	-C %{objdir} \
	%{?with_verbose:V=1} \
	DEPMOD=%{DepMod} \
	INSTALL_MOD_PATH=$RPM_BUILD_ROOT \
	INSTALL_FW_PATH=$RPM_BUILD_ROOT/lib/firmware/%{kernel_release} \
	KERNELRELEASE=%{kernel_release}

install -d $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/misc

# create directories which may be missing, to simplyfy %files
install -d $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/kernel/{arch,sound,mm}

# rpm obeys filelinkto checks for ghosted symlinks, convert to files
rm -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{build,source}
touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{build,source}

# no point embed content for %ghost files. empty them
for a in \
	dep{,.bin} \
	alias{,.bin} \
	symbols{,.bin} \
	{pci,usb,ccw,isapnp,input,ieee1394,serio,of}map \
; do
	test -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/modules.$a
	> $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/modules.$a
done

# /boot
install -d $RPM_BUILD_ROOT/boot
cp -a %{objdir}/System.map $RPM_BUILD_ROOT/boot/System.map-%{kernel_release}
%ifarch %{ix86} %{x8664}
cp -a %{objdir}/arch/%{target_arch_dir}/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
install %{objdir}/vmlinux $RPM_BUILD_ROOT/boot/vmlinux-%{kernel_release}
%endif

# ghosted initrd
touch $RPM_BUILD_ROOT%{initrd_dir}/initrd-%{kernel_release}.gz

%if "%{_target_base_arch}" != "%{_arch}"
touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/modules.dep
%endif

# /etc/modrobe.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{kernel_release}

# /usr/src/linux
install -d $RPM_BUILD_ROOT%{_kernelsrcdir}/include/generated
# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al %{srcdir}/COPYING $RPM_BUILD_ROOT/COPYING 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/COPYING
fi

cp -a$l %{srcdir}/* $RPM_BUILD_ROOT%{_kernelsrcdir}
cp -a %{objdir}/Module.symvers $RPM_BUILD_ROOT%{_kernelsrcdir}/Module.symvers-dist
cp -aL %{objdir}/.config $RPM_BUILD_ROOT%{_kernelsrcdir}/config-dist
cp -a %{objdir}/include/generated/autoconf.h $RPM_BUILD_ROOT%{_kernelsrcdir}/include/generated/autoconf-dist.h
cp -a %{objdir}/include/generated/utsrelease.h $RPM_BUILD_ROOT%{_kernelsrcdir}/include/generated
cp -a %{objdir}/include/linux/version.h $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/generated/autoconf.h
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/config.h

# collect module-build files and directories
# Usage: kernel-module-build.pl $rpmdir $fileoutdir
fileoutdir=$(pwd)
cd $RPM_BUILD_ROOT%{_kernelsrcdir}
%{__perl} %{topdir}/kernel-xenU-module-build.pl %{_kernelsrcdir} $fileoutdir
cd -

# move to %{_docdir} so we wouldn't depend on any kernel package for dirs
install -d $RPM_BUILD_ROOT%{_docdir}
mv $RPM_BUILD_ROOT{%{_kernelsrcdir}/Documentation,%{_docdir}/%{name}-%{version}}

rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/dontdiff
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/Makefile
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/*/Makefile
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/*/*/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{kernel_release}
fi

%post
%ifarch ia64
mv -f /boot/efi/vmlinuz{,.old} 2> /dev/null
%{?alt_kernel:mv -f /boot/efi/vmlinuz%{_alt_kernel}{,.old} 2> /dev/null}
ln -sf vmlinuz-%{kernel_release} /boot/efi/vmlinuz
%{?alt_kernel:ln -sf vmlinuz-%{kernel_release} /boot/efi/vmlinuz%{_alt_kernel}}
%endif
mv -f /boot/vmlinuz{,.old} 2> /dev/null
%{?alt_kernel:mv -f /boot/vmlinuz%{_alt_kernel}{,.old} 2> /dev/null}
mv -f /boot/System.map{,.old} 2> /dev/null
%{?alt_kernel:mv -f /boot/System%{_alt_kernel}.map{,.old} 2> /dev/null}
ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz
%{?alt_kernel:ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz%{_alt_kernel}}
ln -sf System.map-%{kernel_release} /boot/System.map
%{?alt_kernel:ln -sf System.map-%{kernel_release} /boot/System.map%{_alt_kernel}}

%depmod %{kernel_release}

%posttrans
# generate initrd after all dependant modules are installed
/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{kernel_release}.gz %{kernel_release}
mv -f %{initrd_dir}/initrd{,.old} 2> /dev/null
%{?alt_kernel:mv -f %{initrd_dir}/initrd%{_alt_kernel}{,.old} 2> /dev/null}
ln -sf initrd-%{kernel_release}.gz %{initrd_dir}/initrd
%{?alt_kernel:ln -sf initrd-%{kernel_release}.gz %{initrd_dir}/initrd%{_alt_kernel}}

# update boot loaders when old package files are gone from filesystem
if [ -x /sbin/update-grub -a -f /etc/sysconfig/grub ]; then
	if [ "$(. /etc/sysconfig/grub; echo ${UPDATE_GRUB:-no})" = "yes" ]; then
		/sbin/update-grub >/dev/null
	fi
fi
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{kernel_release}.gz --install %{kernel_release} --banner "PLD Linux (%{pld_release})%{?alt_kernel: / %{alt_kernel}}"
fi
if [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post vmlinux
mv -f /boot/vmlinux{,.old} 2> /dev/null
%{?alt_kernel:mv -f /boot/vmlinux-%{alt_kernel}{,.old} 2> /dev/null}
ln -sf vmlinux-%{kernel_release} /boot/vmlinux
%{?alt_kernel:ln -sf vmlinux-%{kernel_release} /boot/vmlinux-%{alt_kernel}}

%post headers
ln -snf %{basename:%{_kernelsrcdir}} %{_prefix}/src/linux%{_alt_kernel}

%postun headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux%{_alt_kernel} ]; then
		if [ "$(readlink %{_prefix}/src/linux%{_alt_kernel})" = "linux%{_alt_kernel}-%{version}" ]; then
			rm -f %{_prefix}/src/linux%{_alt_kernel}
		fi
	fi
fi

%triggerin module-build -- %{name} = %{epoch}:%{version}-%{release}
ln -sfn %{_kernelsrcdir} /lib/modules/%{kernel_release}/build
ln -sfn %{_kernelsrcdir} /lib/modules/%{kernel_release}/source

%triggerun module-build -- %{name} = %{epoch}:%{version}-%{release}
if [ "$1" = 0 ]; then
	rm -f /lib/modules/%{kernel_release}/{build,source}
fi

%files
%defattr(644,root,root,755)
/boot/vmlinuz-%{kernel_release}
/boot/System.map-%{kernel_release}
%ghost %{initrd_dir}/initrd-%{kernel_release}.gz
/lib/firmware/%{kernel_release}

%dir /lib/modules/%{kernel_release}
%dir /lib/modules/%{kernel_release}/kernel
/lib/modules/%{kernel_release}/kernel/arch
/lib/modules/%{kernel_release}/kernel/crypto
/lib/modules/%{kernel_release}/kernel/drivers
%if %{have_drm}
%exclude /lib/modules/%{kernel_release}/kernel/drivers/gpu
%endif
/lib/modules/%{kernel_release}/kernel/fs
/lib/modules/%{kernel_release}/kernel/kernel
/lib/modules/%{kernel_release}/kernel/lib
/lib/modules/%{kernel_release}/kernel/net
/lib/modules/%{kernel_release}/kernel/mm
%if %{have_sound}
%dir /lib/modules/%{kernel_release}/kernel/sound
/lib/modules/%{kernel_release}/kernel/sound/ac97_bus.ko*
/lib/modules/%{kernel_release}/kernel/sound/sound*.ko*
%ifnarch sparc
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/cx88/cx88-alsa.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/em28xx/em28xx-alsa.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/saa7134/saa7134-alsa.ko*
%endif
%endif
%dir /lib/modules/%{kernel_release}/misc
%if %{with myown}
/lib/modules/%{kernel_release}/kernel/sound
%endif

%dir %{_sysconfdir}/modprobe.d/%{kernel_release}

# provided by build
/lib/modules/%{kernel_release}/modules.order
/lib/modules/%{kernel_release}/modules.builtin

# rest modules.* are ghost (regenerated by post depmod -a invocation)
%ghost /lib/modules/%{kernel_release}/modules.alias
%ghost /lib/modules/%{kernel_release}/modules.alias.bin
%ghost /lib/modules/%{kernel_release}/modules.ccwmap
%ghost /lib/modules/%{kernel_release}/modules.dep
%ghost /lib/modules/%{kernel_release}/modules.dep.bin
%ghost /lib/modules/%{kernel_release}/modules.ieee1394map
%ghost /lib/modules/%{kernel_release}/modules.inputmap
%ghost /lib/modules/%{kernel_release}/modules.isapnpmap
%ghost /lib/modules/%{kernel_release}/modules.ofmap
%ghost /lib/modules/%{kernel_release}/modules.pcimap
%ghost /lib/modules/%{kernel_release}/modules.seriomap
%ghost /lib/modules/%{kernel_release}/modules.symbols
%ghost /lib/modules/%{kernel_release}/modules.symbols.bin
%ghost /lib/modules/%{kernel_release}/modules.usbmap

# symlinks pointing to kernelsrcdir
%ghost /lib/modules/%{kernel_release}/build
%ghost /lib/modules/%{kernel_release}/source

%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{kernel_release}

%files headers -f files.headers_exclude_kbuild
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/include
%dir %{_kernelsrcdir}/arch
%dir %{_kernelsrcdir}/arch/[!K]*
%{_kernelsrcdir}/arch/*/include
%dir %{_kernelsrcdir}/security
%dir %{_kernelsrcdir}/security/selinux
%{_kernelsrcdir}/security/selinux/include
%{_kernelsrcdir}/config-dist
%{_kernelsrcdir}/Module.symvers-dist

%files module-build -f files.mb_include_modulebuild_and_dirs
%defattr(644,root,root,755)
%ifarch ppc ppc64
%{_kernelsrcdir}/arch/powerpc/lib/crtsavres.*
%endif
%exclude %dir %{_kernelsrcdir}/arch/m68knommu
%exclude %dir %{_kernelsrcdir}/arch/um
%{_kernelsrcdir}/arch/*/kernel/asm-offsets*
%{_kernelsrcdir}/arch/*/kernel/sigframe*.h
%{_kernelsrcdir}/drivers/lguest/lg.h
%{_kernelsrcdir}/kernel/bounds.c
%dir %{_kernelsrcdir}/scripts
%{_kernelsrcdir}/scripts/Kbuild.include
%{_kernelsrcdir}/scripts/Makefile*
%{_kernelsrcdir}/scripts/basic
%{_kernelsrcdir}/scripts/kconfig
%{_kernelsrcdir}/scripts/mkcompile_h
%{_kernelsrcdir}/scripts/mkmakefile
%{_kernelsrcdir}/scripts/mod
%{_kernelsrcdir}/scripts/module-common.lds
%{_kernelsrcdir}/scripts/setlocalversion
%{_kernelsrcdir}/scripts/*.c
%{_kernelsrcdir}/scripts/*.sh
%dir %{_kernelsrcdir}/scripts/selinux
%{_kernelsrcdir}/scripts/selinux/Makefile
%dir %{_kernelsrcdir}/scripts/selinux/genheaders
%{_kernelsrcdir}/scripts/selinux/genheaders/Makefile
%{_kernelsrcdir}/scripts/selinux/genheaders/*.c
%dir %{_kernelsrcdir}/scripts/selinux/mdp
%{_kernelsrcdir}/scripts/selinux/mdp/Makefile
%{_kernelsrcdir}/scripts/selinux/mdp/*.c
%exclude %dir %{_kernelsrcdir}/security
%exclude %dir %{_kernelsrcdir}/security/selinux

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}-%{version}

%{_docdir}/%{name}-%{version}/[!jkz]*
%{_docdir}/%{name}-%{version}/[jkz]*.txt
%{_docdir}/%{name}-%{version}/kbuild
%{_docdir}/%{name}-%{version}/kdump
%{_docdir}/%{name}-%{version}/kvm
%lang(ja) %{_docdir}/%{name}-%{version}/ja_JP
%lang(ko) %{_docdir}/%{name}-%{version}/ko_KR
%lang(zh_CN) %{_docdir}/%{name}-%{version}/zh_CN
%endif

%if %{with source}
%files source -f files.source_exclude_modulebuild_and_dirs
%defattr(644,root,root,755)
%{_kernelsrcdir}/arch/*/[!Mik]*
%{_kernelsrcdir}/arch/*/kernel/[!M]*
%{_kernelsrcdir}/arch/ia64/install.sh
%{_kernelsrcdir}/arch/m68k/ifpsp060/[!M]*
%{_kernelsrcdir}/arch/m68k/ifpsp060/MISC
%{_kernelsrcdir}/arch/m68k/install.sh
%{_kernelsrcdir}/arch/parisc/install.sh
%{_kernelsrcdir}/arch/x86/ia32/[!M]*
%{_kernelsrcdir}/arch/ia64/kvm
%{_kernelsrcdir}/arch/powerpc/kvm
%ifarch ppc ppc64
%exclude %{_kernelsrcdir}/arch/powerpc/lib/crtsavres.*
%endif
%{_kernelsrcdir}/arch/s390/kvm
%{_kernelsrcdir}/arch/x86/kvm
%exclude %{_kernelsrcdir}/arch/*/kernel/asm-offsets*
%exclude %{_kernelsrcdir}/arch/*/kernel/sigframe*.h
%exclude %{_kernelsrcdir}/drivers/lguest/lg.h
%{_kernelsrcdir}/block
%{_kernelsrcdir}/crypto
%{_kernelsrcdir}/drivers
%{_kernelsrcdir}/firmware
%{_kernelsrcdir}/fs
%if %{with grsecurity} && %{without rescuecd}
%{_kernelsrcdir}/grsecurity
%endif
%{_kernelsrcdir}/init
%{_kernelsrcdir}/ipc
%{_kernelsrcdir}/kernel
%exclude %{_kernelsrcdir}/kernel/bounds.c
%{_kernelsrcdir}/lib
%{_kernelsrcdir}/mm
%{_kernelsrcdir}/net
%{_kernelsrcdir}/virt
%{_kernelsrcdir}/samples
%{_kernelsrcdir}/scripts/*
%exclude %{_kernelsrcdir}/scripts/Kbuild.include
%exclude %{_kernelsrcdir}/scripts/Makefile*
%exclude %{_kernelsrcdir}/scripts/basic
%exclude %{_kernelsrcdir}/scripts/kconfig
%exclude %{_kernelsrcdir}/scripts/mkcompile_h
%exclude %{_kernelsrcdir}/scripts/mkmakefile
%exclude %{_kernelsrcdir}/scripts/mod
%exclude %{_kernelsrcdir}/scripts/module-common.lds
%exclude %{_kernelsrcdir}/scripts/setlocalversion
%exclude %{_kernelsrcdir}/scripts/*.c
%exclude %{_kernelsrcdir}/scripts/*.sh
%exclude %dir %{_kernelsrcdir}/scripts/selinux
%exclude %{_kernelsrcdir}/scripts/selinux/Makefile
%exclude %dir %{_kernelsrcdir}/scripts/selinux/genheaders
%exclude %{_kernelsrcdir}/scripts/selinux/genheaders/Makefile
%exclude %{_kernelsrcdir}/scripts/selinux/genheaders/*.c
%exclude %dir %{_kernelsrcdir}/scripts/selinux/mdp
%exclude %{_kernelsrcdir}/scripts/selinux/mdp/Makefile
%exclude %{_kernelsrcdir}/scripts/selinux/mdp/*.c
%{_kernelsrcdir}/sound
%{_kernelsrcdir}/security
%exclude %{_kernelsrcdir}/security/selinux/include
%{_kernelsrcdir}/tools
%{_kernelsrcdir}/usr
%{_kernelsrcdir}/COPYING
%{_kernelsrcdir}/CREDITS
%{_kernelsrcdir}/MAINTAINERS
%{_kernelsrcdir}/README
%{_kernelsrcdir}/REPORTING-BUGS
%endif
