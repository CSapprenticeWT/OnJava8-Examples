# Requires Python 3.5 or greater
# (c)2016 MindView LLC: see Copyright.txt
# We make no guarantees that this code is fit for any purpose.
# Visit http://mindviewinc.com/Books/OnJava/ for more book information.
"""
ToDo:
    - Validate errors (.err files, not just .out files)
    - Are there any duplicate file names throughout the book?
"""
import sys
from pathlib import Path
import re
import textwrap
from enum import Enum, unique

def trace(str): pass
# trace = print

maxlinewidth = 59
current_dir_name = Path.cwd().stem

word_only = re.compile("[A-Za-z]+")

def trim(block):
    trimmed = "\n".join([ln.rstrip() for ln in block.splitlines()])
    return trimmed.strip()

class Adjuster:
    def adjust(self, input_text): pass

class IgnoreDigits(Adjuster):
    def adjust(self, input_text):
        trace("Ignoring digits")
        return trim(re.sub("-?\d", "", input_text))

class IgnoreMemoryAddresses(Adjuster):
    def adjust(self, input_text):
        return trim(memlocation.sub("", input_text))

class RemoveCharacters(Adjuster):
    def __init__(self, chars_to_remove):
        self.chars_to_remove = chars_to_remove
    def adjust(self, input_text):
        for c in self.chars_to_remove:
            input_text = input_text.replace(c, "")
        return input_text

class CompareSortedLines(Adjuster):
    def adjust(self, input_text):
        return "\n".join(sorted(input_text.splitlines())).strip()

class CompareSortedWords(Adjuster):
    def adjust(self, input_text):
        return "\n".join(sorted(input_text.split())).strip()

class CompareUniqueLines(Adjuster):
    def adjust(self, input_text):
        return "\n".join(sorted(list(set(input_text.splitlines()))))

class CompareUniqueWords(Adjuster):
    # Fairly extreme but will still reveal significant changes
    def adjust(self, input_text):
        return "\n".join(sorted(set(input_text.split())))

class CompareWordsOnly(Adjuster):
    # Fairly extreme but will still reveal significant changes
    def adjust(self, input_text):
        return "\n".join(
            sorted([w for w in input_text.split()
                    if word_only.fullmatch(w)]))

class IgnoreLines(Adjuster):
    def __init__(self, *lines_to_ignore):
        self.lines_to_ignore = lines_to_ignore
    def adjust(self, input_text):
        lines = input_text.splitlines()
        for ignore in sorted(list(self.lines_to_ignore), reverse=True):
            ignore = ignore - 1 # Compensate for zero indexing
            trace("ignoring line %d: %s" % (ignore, lines[ignore]))
            del lines[ignore]
        return "\n".join(lines)


match_adjustments = {
    "ToastOMatic.java" : CompareSortedLines(),
    "ThreadVariations.java" : CompareSortedLines(),
    "ActiveObjectDemo.java" : [CompareSortedLines(), IgnoreDigits()],
    "Interrupting.java" : CompareSortedLines(),
    "SyncObject.java" : CompareSortedLines(),
    "UseCaseTracker.java" : CompareSortedLines(),
    "AtUnitComposition.java" : CompareSortedLines(),
    "AtUnitExample1.java" : CompareSortedLines(),
    "AtUnitExample2.java" : CompareSortedLines(),
    "AtUnitExample3.java" : CompareSortedLines(),
    "AtUnitExample5.java" : CompareSortedLines(),
    "AtUnitExternalTest.java" : CompareSortedLines(),
    "HashSetTest.java" : CompareSortedLines(),
    "StackLStringTest.java" : CompareSortedLines(),
    "WaxOMatic2.java" : CompareSortedLines(),

    "ForEach.java" : CompareSortedWords(),
    "PetCount4.java" : [RemoveCharacters("{}"), CompareSortedWords()],

    "CachedThreadPool.java" : CompareWordsOnly(),
    "FixedThreadPool.java" : CompareWordsOnly(),
    "MoreBasicThreads.java" : CompareWordsOnly(),
    "ConstantSpecificMethod.java" : CompareWordsOnly(),

    "BankTellerSimulation.java" : [CompareWordsOnly(), CompareUniqueWords()],

    "MapComparisons.java" : IgnoreDigits(),
    "ListComparisons.java" : IgnoreDigits(),
    "NotifyVsNotifyAll.java" : IgnoreDigits(),
    "SelfManaged.java" : IgnoreDigits(),
    "SimpleMicroBenchmark.java" : IgnoreDigits(),
    "SimpleThread.java" : IgnoreDigits(),
    "SleepingTask.java" : IgnoreDigits(),
    "ExchangerDemo.java" : IgnoreDigits(),
    "Compete.java" : IgnoreDigits(),
    "MappedIO.java" : IgnoreDigits(),
    "Directories.java" : IgnoreDigits(),
    "Find.java" : IgnoreDigits(),
    "PathAnalysis.java" : IgnoreDigits(),
    "TreeWatcher.java" : IgnoreDigits(),
    "Mixins.java" : IgnoreDigits(),
    "ListPerformance.java" : IgnoreDigits(),
    "MapPerformance.java" : IgnoreDigits(),
    "SetPerformance.java" : IgnoreDigits(),
    "SynchronizationComparisons.java" : IgnoreDigits(),
    "AtomicityTest.java" : IgnoreDigits(),
    "TypesForSets.java" : IgnoreDigits(),
    "PrintableLogRecord.java" : IgnoreDigits(),
    "LockingMappedFiles.java" : IgnoreDigits(),

    "Conversion.java" : IgnoreLines(27, 28),
    "DynamicProxyMixin.java" : IgnoreLines(2),
    "PreferencesDemo.java" : IgnoreLines(5),

    "SerialNumberChecker.java" : [IgnoreDigits(), CompareUniqueLines()],
    "EvenSupplier.java" : [IgnoreDigits(), CompareUniqueLines()],

    "FillingLists.java" : [ IgnoreMemoryAddresses(), CompareSortedWords() ],

    "SimpleDaemons.java" : [ IgnoreMemoryAddresses(), IgnoreDigits() ],
    "CaptureUncaughtException.java" : [
        IgnoreMemoryAddresses(), IgnoreDigits(), CompareUniqueLines() ],

    "CarBuilder.java" : [ IgnoreDigits(), CompareUniqueLines() ],
    "CloseResource.java" : [ CompareUniqueLines() ],

    "SpringDetector.java" : [ IgnoreDigits(), CompareSortedWords() ],

    "PipedIO.java" : [ CompareUniqueWords() ],

    "ExplicitCriticalSection.java" : IgnoreDigits(),
}


translate_file_name = {
    "ApplyTest.java": "Apply.java",
    "FillTest.java": "Fill.java",
    "Fill2Test.java": "Fill2.java",
    "ClassInInterface$Test.java": "ClassInInterface.java",
    "TestBed$Tester.java": "TestBed.java",
}


memlocation = re.compile("@[0-9a-z]{5,7}")
datestamp1 = re.compile("(?:[MTWFS][a-z]{2} ){0,1}[JFMASOND][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}")
datestamp2 = re.compile("[JFMASOND][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} (:?AM|PM)")
varying = [ memlocation, datestamp1, datestamp2 ]


# Result of Duet.validate():
Valid = Enum('Valid',
    'exact  varying  execute_to_see  selected_lines  fail')


class Duet:
    """
    Holds embedded and generated output. Also original file content, and
    "adjusted" output for comparison.
    """

    def __init__(self, out_filename):
        if not out_filename.suffix == ".out" or out_filename.suffix == ".err":
            print("Error: argument to Duet() must end with '.out' or '.err'")
            print("Argument was {}".format(out_filename))
            sys.exit()
        self.java_file = None # Full contents of Java code file
        self.java_slugline = None # First (marker) line of Java code file

        self.out_path = out_filename.with_suffix(".out")
        self.out = None
        if self.out_path.exists():
            self.out = self.out_path.read_text()
            trace("{} file exists".format(self.out_path))

        self.err_path = out_filename.with_suffix(".err")
        self.errors = None
        if self.err_path.exists():
            self.errors = self.err_path.read_text()
            print("{} file exists".format(self.err_path))

        self.java_path = self.calculate_java_path()
        self.embedded = self.embedded_output()
        self.ignore = False
        if "{IgnoreOutput}" in self.java_file:
            self.ignore = True
            trace("Ignoring .out for {}".format(self.java_path))
            return
        self.generated = self.out_path.read_text().strip()
        self.generated = self.fill_to_width(self.generated)
        self.embedded_adjusted = self.adjust(self.embedded)
        self.generated_adjusted = self.adjust(self.generated)

    def calculate_java_path(self):

        def __java_filename(out_pieces):
            path_components = out_pieces.split(".", out_pieces.count(".") - 1)
            # path_components[-1] = path_components[-1].replace(".out", ".java")
            # path_components[-1] = path_components[-1].replace(".err", ".java")
            return path_components

        _java_path = self.out_path.with_suffix(".java")
        jfn = __java_filename(_java_path.parts[-1])
        # jfn = __java_filename(self.out_path.parts[-1])
        jpath = list(self.out_path.parts[:-1]) + list(jfn)
        if len(jpath) > 1 and jpath[0] == jpath[1]:
            del jpath[0]
        if jpath[0] == current_dir_name:
            del jpath[0]
        if jpath[-1] in translate_file_name:
            jpath[-1] = translate_file_name[jpath[-1]]
        return Path(*jpath)


    def embedded_output(self):
        find_output = re.compile(r"/\* (Output:.*)\*/", re.DOTALL) # should space be \s+ ??
        with self.java_path.open() as java:
            self.java_file = java.read()
            self.java_slugline = self.java_file.strip().splitlines()[0]
            output = find_output.search(self.java_file)
            if not output:
                trace("No embedded output: in {}".format(self.java_path))
                return None
            lines = output.group(1).strip().splitlines()
            self.output_tag = lines[0]
            return ("\n".join(lines[1:])).strip()


    @staticmethod
    def fill_to_width(text):
        result = ""
        for line in text.splitlines():
            result += textwrap.fill(line, width=maxlinewidth) + "\n"
        return result.strip()


    def __repr__(self):
        # result = "\n" + str(self.output_tag)
        result = "\n" + str(self.java_path).center(60, "=") + "\n" + self.embedded
        result += "\n" + str(self.out_path).center(60, "-") + "\n" + self.generated
        result += "\n" + (str(self.java_path) +
            "(adjusted)").center(60, "-") + "\n" + str(self.embedded_adjusted)
        result += "\n" + (str(self.out_path) +
            "(adjusted)").center(60, "-") + "\n" + str(self.generated_adjusted)

        difflines = []
        embedded_adjusted_lines = self.embedded_adjusted.splitlines()
        generated_adjusted_lines = self.generated_adjusted.splitlines()
        trace(str(self.java_path))
        trace("len embedded_adjusted %d len generated_adjusted %d" %
              (len(embedded_adjusted_lines), len(generated_adjusted_lines)))
        for n, line in enumerate(embedded_adjusted_lines):
            try:
                if not line == generated_adjusted_lines[n]:
                    difflines.append(">--------<")
                    difflines.append("embedded_adjusted:  " + line)
                    difflines.append("generated_adjusted: " + generated_adjusted_lines[n])
            except:
                continue
        if difflines:
            result += "\n" + "\n".join(difflines)

        return result


    @staticmethod
    def strip_varying(text):
        for pat in varying:
            text = pat.sub("", text)
        return text


    def adjust(self, output):
        output = output.replace("\0", "NUL")
        if self.java_path.name not in match_adjustments:
            return output
        trace("adjusting %s" % self.java_path.name)
        strategy = match_adjustments[self.java_path.name]
        if isinstance(strategy, Adjuster):
            return strategy.adjust(output)
        assert isinstance(strategy, list)
        for strat in strategy:
            output = strat.adjust(output)
        return output


    def validate(self):
        if "(Execute to see)" in self.output_tag:
            return Valid.execute_to_see
        if "(None)" in self.output_tag: ### This should no longer be necessary
            assert false, "(None) in output_tag " + self
        if "Output: (First" in self.output_tag:          ### This is temporary ###
            return Valid.selected_lines
        if self.generated_adjusted == self.embedded_adjusted:
            return Valid.exact
        if isinstance(self.generated_adjusted, str):
            if (Duet.strip_varying(self.generated_adjusted) ==
                Duet.strip_varying(self.embedded_adjusted)):
                return Valid.varying
        return Valid.fail