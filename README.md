# Chaos-Aided Quantization Index Modulation

# Abstract
Quantization Index Modulation (QIM) is widely recognized as an efficient and practical steganographic technique. Meanwhile, chaos-based steganography exploits the inherent unpredictability and complexity of chaotic systems to generate pseudorandom sequences. These sequences are commonly used as dithers in quantization-based embedding, effectively enhancing the security and imperceptibility of the hidden message. Howerver, Traditional QIM techniques often alter the statistical properties of the host signal, making them vulnerable to detection through statistical steganalysis, while chaotic steganography introduces significant distortion or complexity. By leverageing chaos theory, we introduce the Chaos-QIM (Quantization Index Modulation) technique. Initially, a chaotic system generates a random sequence, which is then transformed into a uniform distribution using modulo lattice operation. Chaos-QIM utilizes this uniform sequence as dither in the quantization process, ensuring the resulting stego-signal is statistically indistinguishable from the original signal. In the paper, We rigorously prove both the statistical indistinguishability of the stego-signal and the system’s resistance to attack. A comprehensive security analysis highlights Chaos-QIM’s resistance against statistical steganalysis techniques.

# Codes
- Chaos-QIM: Chaos-Aided Quantization Index Modulation
- QIM: Quantization Index Modulation based on lattice
- SDCVP: Lattice Encode and Decode
- Logistic: Transform sequence to uniform distribution
